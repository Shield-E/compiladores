from collections import defaultdict, deque
from itertools import count

from compila.automata import FiniteAutomata, State
from compila.parser.parser_ll1 import ParserLL1
from compila.regexp.regex_grammar import RegexGrammar
from compila.regexp.regex_tokenizer import RegexTokenizer
from compila.regexp.regex_tree import *

regex_tokenizer = RegexTokenizer()
regex_grammar = RegexGrammar()
regex_parser = ParserLL1(regex_tokenizer, regex_grammar)


def compile(expression: str) -> FiniteAutomata:
    """
    Converts a regular expression into equivalent Finite Automata.
    """

    node = regex_parser.analyze(expression)
    tree = node.syn_tree

    tree = _anotate_tree(tree)
    followpos = _calculate_followpos(tree)
    leafs = get_leafs(tree)

    alphabet = [leaf.symbol for leaf in leafs]

    symbol_tags = defaultdict(set)
    for leaf in leafs:
        symbol_tags[leaf.symbol] |= leaf.firstpos

    states, transitions = _get_automata_parameters(
        first_tagset=frozenset(tree.firstpos),
        final_leaf_tag=tuple(tree.children[1].firstpos)[0],
        alphabet=alphabet,
        followpos=followpos,
        symbol_tags=symbol_tags,
    )

    return FiniteAutomata(
        states=states, transitions=transitions, alphabet=alphabet, initial_state_index=0
    )


def _calculate_followpos(tree: RegexNode) -> defaultdict[int, set]:
    followpos = defaultdict(set)
    _recursive_followpos(tree, followpos)
    return dict(followpos)


def _recursive_followpos(tree: RegexNode, followpos: defaultdict[int, set]):
    if tree is None:
        return

    if isinstance(tree, ClosureNode):
        for i in tree.lastpos:
            for j in tree.firstpos:
                followpos[i].add(j)
        _recursive_followpos(tree.children[0], followpos)

    elif isinstance(tree, ConcatNode):
        left_node = tree.children[0]
        right_node = tree.children[1]
        for i in left_node.lastpos:
            for j in right_node.firstpos:
                followpos[i].add(j)
        _recursive_followpos(left_node, followpos)
        _recursive_followpos(right_node, followpos)

    elif isinstance(tree, UnionNode):
        left_node = tree.children[0]
        right_node = tree.children[1]
        _recursive_followpos(left_node, followpos)
        _recursive_followpos(right_node, followpos)


def _anotate_tree(tree: RegexNode) -> RegexNode:
    tree = ConcatNode(tree, EndMarkerNode())
    _recursive_anotate_tree(tree, 0)
    return tree


def _recursive_anotate_tree(tree: RegexNode, tag: int) -> int:
    """
    Recursive function to calculate firstpos and lastpos for all trees.
    """
    if isinstance(tree, EpsilonNode):
        tree.nullable = True
        return tag

    if isinstance(tree, (SymbolNode, EndMarkerNode)):
        tree.firstpos = {tag}
        tree.lastpos = {tag}
        tree.nullable = False
        return tag + 1

    if isinstance(tree, UnionNode):
        for node in tree.children:
            tag = _recursive_anotate_tree(node, tag)
        tree.firstpos = set.union(*[node.firstpos for node in tree.children])
        tree.lastpos = set.union(*[node.lastpos for node in tree.children])
        tree.nullable = any([node.nullable for node in tree.children])
        return tag

    if isinstance(tree, ConcatNode):
        for node in tree.children:
            tag = _recursive_anotate_tree(node, tag)

        left_node = tree.children[0]
        right_node = tree.children[1]

        if left_node.nullable:
            tree.firstpos = left_node.firstpos | right_node.firstpos
        else:
            tree.firstpos = left_node.firstpos

        if right_node.nullable:
            tree.lastpos = left_node.lastpos | right_node.lastpos
        else:
            tree.lastpos = right_node.lastpos

        tree.nullable = left_node.nullable and right_node.nullable
        return tag

    if isinstance(tree, ClosureNode):
        tag = _recursive_anotate_tree(tree.children[0], tag)
        tree.nullable = True
        tree.firstpos = tree.children[0].firstpos
        tree.lastpos = tree.children[0].lastpos
        return tag


def _get_automata_parameters(
    *, first_tagset, final_leaf_tag, alphabet, followpos, symbol_tags
):
    states = []
    transitions = []

    tagset_to_index = defaultdict(
        count().__next__
    )  # gives a new index for new elements
    tagset_queue = deque()
    tagset_queue.appendleft(first_tagset)

    while tagset_queue:
        tagset = tagset_queue.pop()

        i = tagset_to_index[tagset]
        is_final = final_leaf_tag in tagset
        states.append(State(f"q{i}", is_final))

        for symbol in alphabet:
            u = frozenset()
            for i in tagset & symbol_tags[symbol]:
                u |= followpos[i]

            if u not in tagset_to_index:
                tagset_queue.appendleft(u)

            transition = (tagset_to_index[tagset], symbol, tagset_to_index[u])
            transitions.append(transition)

    return states, transitions


def get_leafs(tree):
    if isinstance(tree, SymbolNode):
        return [tree]

    leafs = []
    for node in tree.children:
        leafs.extend(get_leafs(node))
    return leafs
