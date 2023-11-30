from compila.constants import ALPHANUMERIC, EPSILON
from compila.parser.grammar import Grammar
from compila.parser.production import Production
from compila.regexp.regex_tree import *


class RegexGrammar(Grammar):
    def __init__(self):
        productions = self.create_productions()
        super().__init__(productions)

    def create_productions(self):
        productions = [
            Production("EXPRESSION", ["OR", op_expression]),
            Production("OR", ["AND", op0_or, "OR1", op1_or]),
            Production("OR1", ["|", "AND", op2_or, "OR1", op3_or]),
            Production("OR1", [EPSILON, op4_or]),
            Production("AND", ["UNITY", op0_and, "AND1", op1_and]),
            Production("AND1", ["UNITY", op2_and, "AND1", op1_and]),
            Production("AND1", [EPSILON, op3_and]),
            Production("UNITY", ["GROUP", op0_unity, "UNITY1", op1_unity]),
            Production("UNITY1", ["*", op2_unity]),
            Production("UNITY1", ["+", op3_unity]),
            Production("UNITY1", ["?", op4_unity]),
            Production("UNITY1", [EPSILON, op5_unity]),
            Production("GROUP", ["SYMBOL", op0_group]),
            Production("GROUP", ["(", "EXPRESSION", ")", op1_group]),
            Production("GROUP", ["\\", "SPECIAL_SYMBOL", op2_group]),
        ]

        regex_safe_symbols = " !@#$%¨&/-={,.;}'[]\""
        for i in ALPHANUMERIC + regex_safe_symbols:
            prod = Production("SYMBOL", [i, op_symbol])
            productions.append(prod)

        for i in "+*?\\|()":
            prod = Production("SPECIAL_SYMBOL", [i, op_symbol])
            productions.append(prod)

        return productions


# Semantic rules:
def op0_group(parser, origin, target):
    symbol = target[0]
    origin.syn_tree = symbol.syn_tree


def op1_group(parser, origin, target):
    expression = target[1]
    origin.syn_tree = expression.syn_tree


def op2_group(parser, origin, target):
    special_symbol = target[1]
    origin.syn_tree = special_symbol.syn_tree

#
def op0_unity(parser, origin, target):
    group, unity1 = target
    unity1.her_tree = group.syn_tree


def op1_unity(parser, origin, target):
    group, unity1 = target
    origin.syn_tree = unity1.syn_tree


def op2_unity(parser, origin, target):
    origin.syn_tree = ClosureNode(origin.her_tree)


def op3_unity(parser, origin, target):
    origin.syn_tree = ConcatNode(origin.her_tree, ClosureNode(origin.her_tree))


def op4_unity(parser, origin, target):
    origin.syn_tree = UnionNode(EpsilonNode(), origin.her_tree)


def op5_unity(parser, origin, target):
    origin.syn_tree = origin.her_tree


#
def op0_and(parser, origin, target):
    unity, and1 = target
    and1.her_tree = unity.syn_tree


def op1_and(parser, origin, target):
    and1 = target[1]
    origin.syn_tree = and1.syn_tree


def op2_and(parser, origin, target):
    unity, and1 = target
    and1.her_tree = ConcatNode(origin.her_tree, unity.syn_tree)


def op3_and(parser, origin, _):
    origin.syn_tree = origin.her_tree


#
def op0_or(parser, origin, target):
    _and, or1 = target
    or1.her_tree = _and.syn_tree


def op1_or(parser, origin, target):
    or1 = target[1]
    origin.syn_tree = or1.syn_tree


def op2_or(parser, origin, target):
    _, _and, or1_1 = target
    or1_1.her_tree = UnionNode(origin.her_tree, _and.syn_tree)


def op3_or(parser, origin, target):
    or1_1 = target[2]
    origin.syn_tree = or1_1.syn_tree


def op4_or(parser, origin, target):
    origin.syn_tree = origin.her_tree


#
def op_expression(parser, origin, target):
    _or = target[0]
    origin.syn_tree = _or.syn_tree


def op_symbol(parser, origin, target):
    char = target[0]
    origin.syn_tree = SymbolNode(char)
