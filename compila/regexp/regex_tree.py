from treelib import Tree


class RegexNode:
    def __init__(self, *children):
        self.children = list(children)
        self.firstpos = set()
        self.lastpos = set()
        self.nullable = False

    def tree_str(self):
        """
        Returns a string that represents the tree graphically.
        """

        def representation(node):
            if isinstance(node, UnionNode):
                return "or"
            elif isinstance(node, ConcatNode):
                return "."
            elif isinstance(node, SymbolNode):
                return node.symbol
            elif isinstance(node, ClosureNode):
                return "*"
            else:
                return ""

        tree = Tree()
        stack = [self]

        tree.create_node(representation(self), hash(self))
        while stack:
            node = stack.pop()
            for child in node.children:
                tree.create_node(representation(child), hash(child), parent=hash(node))
                stack.append(child)

        return tree

    def __str__(self) -> str:
        return str(self.tree_str())


class UnionNode(RegexNode):
    pass


class ConcatNode(RegexNode):
    pass


class ClosureNode(RegexNode):
    pass


class EpsilonNode(RegexNode):
    pass


class EndMarkerNode(RegexNode):
    pass


class SymbolNode(RegexNode):
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
