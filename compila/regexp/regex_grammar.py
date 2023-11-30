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

        regex_safe_symbols = " \n!@#$%¨&/-={,.;}'[]\"<>"
        for i in ALPHANUMERIC + regex_safe_symbols:
            prod = Production("SYMBOL", [i, op_symbol])
            productions.append(prod)

        for i in "+*?\\|()":
            prod = Production("SPECIAL_SYMBOL", [i, op_symbol])
            productions.append(prod)

        return productions


# Semantic rules:
def op0_group(group, symbol):
    group.syn_tree = symbol.syn_tree


def op1_group(group, _0, expression, _1):
    group.syn_tree = expression.syn_tree


def op2_group(group, _, special_symbol):
    group.syn_tree = special_symbol.syn_tree


#
def op0_unity(unity, group, unity1):
    unity1.her_tree = group.syn_tree


def op1_unity(unity, group, unity1):
    unity.syn_tree = unity1.syn_tree


def op2_unity(unity, _):
    unity.syn_tree = ClosureNode(unity.her_tree)


def op3_unity(unity, _):
    unity.syn_tree = ConcatNode(unity.her_tree, ClosureNode(unity.her_tree))


def op4_unity(unity, _):
    unity.syn_tree = UnionNode(EpsilonNode(), unity.her_tree)


def op5_unity(unity, _):
    unity.syn_tree = unity.her_tree


#
def op0_and(_and, unity, and1):
    and1.her_tree = unity.syn_tree


def op1_and(_and, unity, and1):
    _and.syn_tree = and1.syn_tree


def op2_and(_and, unity, and1):
    and1.her_tree = ConcatNode(_and.her_tree, unity.syn_tree)


def op3_and(_and, _):
    _and.syn_tree = _and.her_tree


#
def op0_or(_or, _and, or1):
    or1.her_tree = _and.syn_tree


def op1_or(_or, _and, or1):
    _or.syn_tree = or1.syn_tree


def op2_or(or1_0, _, _and, or1_1):
    or1_1.her_tree = UnionNode(or1_0.her_tree, _and.syn_tree)


def op3_or(or1_0, _, _and, or1_1):
    or1_0.syn_tree = or1_1.syn_tree


def op4_or(or1, _):
    or1.syn_tree = or1.her_tree


#
def op_expression(expression, _or):
    expression.syn_tree = _or.syn_tree


def op_symbol(symbol, char):
    symbol.syn_tree = SymbolNode(char)
