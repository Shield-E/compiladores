from compila.constants import EPSILON
from compila.parser.grammar import Grammar
from compila.parser.production import Production
from compila.error import CompilaSemanticalError
from compila.parser.symbol_table import SymbolTable

from dataclasses import dataclass
from treelib import Tree

def type_rule_0(parser, origin, target):
    target[0].symbol_table = SymbolTable()

def type_rule_1(parser, origin, target):
    target[0].symbol_table = origin.symbol_table

def type_rule_2(parser, origin, target):
    target[1].symbol_table = SymbolTable(origin.symbol_table)

def type_rule_3(parser, origin, target):
    _type = target[0]
    vardecl = target[1]
    vardecl.type = _type.type
    vardecl.symbol_table = origin.symbol_table

def type_rule_4(parser, origin, target):
    origin.type = target[0].token.lexema

def type_rule_5(parser, origin, target):
    symbol = target[0].token.lexema

    if symbol in origin.symbol_table:
        _, _row = origin.symbol_table[symbol]
        error_info = parser.get_error_info(parser.analyzed_input, target[0].token)
        raise CompilaSemanticalError(
            f'Variable "{symbol}" was already declared in row {_row + 1}.',
            *error_info
        )

    row, col = parser.find_row_col(parser.analyzed_input, target[0].token)
    origin.symbol_table.add_symbol(symbol, origin.type, row)

def type_rule_6(parser, origin, target):
    target[0].symbol_table = origin.symbol_table
    target[1].symbol_table = origin.symbol_table

def type_rule_7(parser, origin, target):
    target[2].symbol_table = origin.symbol_table
    target[4].symbol_table = origin.symbol_table
    target[5].symbol_table = origin.symbol_table

def type_rule_8(parser, origin, target):
    target[2].symbol_table = SymbolTable(origin.symbol_table)

def type_rule_9(parser, origin, target):
    target[2].symbol_table = origin.symbol_table
    target[4].symbol_table = origin.symbol_table
    target[6].symbol_table = origin.symbol_table
    target[8].symbol_table = origin.symbol_table

def type_rule_10(parser, origin, target):
    target[6].symbol_table = SymbolTable(origin.symbol_table)

def type_rule_11(parser, origin, target):
    symbol = target[0].token.lexema
    if not symbol in origin.symbol_table:
        error_info = parser.get_error_info(parser.analyzed_input, target[0].token)
        raise CompilaSemanticalError(
            f'Variable "{symbol}" was used but was not declared.',
            *error_info
        )

def type_rule_12(parser, origin, target):
    target[0].symbol_table = origin.symbol_table
    target[2].symbol_table = origin.symbol_table

def type_rule_13(parser, origin, target):
    target[1].symbol_table = origin.symbol_table

def type_rule_14(parser, origin, target):
    target[1].symbol_table = origin.symbol_table
    target[2].symbol_table = origin.symbol_table



class CCLangGrammar(Grammar):
    def __init__(self):
        productions = self.create_productions()
        super().__init__(productions)

    def create_productions(self):
        productions = [
            Production("PROGRAM", [type_rule_0, "STATEMENT"]),
            Production("PROGRAM", [type_rule_0, "FUNCLIST"]),
            Production("PROGRAM", [EPSILON]),

            Production("FUNCLIST", [type_rule_6, "FUNCDEF","FUNCLIST`"]),

            Production("FUNCLIST`", [type_rule_6, "FUNCDEF", "FUNCLIST`"]),
            Production("FUNCLIST`", [EPSILON]),

            Production("FUNCDEF", ["def", "identifier", "(", "PARAMLIST", ")", '{', type_rule_10, break_rule_2, "STATELIST", "}"]),

            Production("INTFLOATSTR", ["int", type_rule_4]),
            Production("INTFLOATSTR", ["float", type_rule_4]),
            Production("INTFLOATSTR", ["str", type_rule_4]),

            Production("PARAMLIST", ["INTFLOATSTR", "identifier", "PARAMLIST`"]),
            Production("PARAMLIST`", ["," , "PARAMLIST"]),
            Production("PARAMLIST`", [EPSILON]),
            Production("PARAMLIST", [EPSILON]),

            Production("STATEMENT", [type_rule_1, "VARDECL", ";"]),
            Production("STATEMENT", [type_rule_1, "ATRIBSTAT", ";"]),
            Production("STATEMENT", [type_rule_1, "PRINTSTAT", ";"]),
            Production("STATEMENT", [type_rule_1, "READSTAT", ";"]),
            Production("STATEMENT", [type_rule_1, "RETURNSTAT", ";"]),
            Production("STATEMENT", [type_rule_1, "IFSTAT"]),
            Production("STATEMENT", [type_rule_1, "FORSTAT"]),
            Production("STATEMENT", [type_rule_2, "{", break_rule_5, "STATELIST", "}"]),
            Production("STATEMENT", ["break", ";", break_rule_1]),
            Production("STATEMENT", [";"]),

            Production("VARDECL", ["INTFLOATSTR", type_rule_3, "VARDECL`"]),

            Production("VARDECL`", ["identifier", type_rule_5, "VARDECL``"]),
            Production("VARDECL``", ["INTCONSTANTLOOP"]),
            Production("VARDECL``", [EPSILON]),

            Production("INTCONSTANTLOOP", ["[", "int_constant", "]", "INTCONSTANTLOOP`"]),

            Production("INTCONSTANTLOOP`", ["INTCONSTANTLOOP"]),
            Production("INTCONSTANTLOOP`", [EPSILON]),

            Production("ATRIBSTAT", [type_rule_12, "LVALUE", "=", "ATRIBSTAT`"]),

            Production("ATRIBSTAT`", [type_rule_1, "EXPRESSION"]),
            Production("ATRIBSTAT`", [type_rule_1, "ALLOCEXPRESSION"]),
            # Production("ATRIBSTAT`", ["#", "FUNCCALL"]),

            # Production("FUNCCALL", ["identifier", "(", "PARAMLISTCALL", ")"]),

            Production("PARAMLISTCALL", ["identifier", "PARAMLISTCALL`"]),
            Production("PARAMLISTCALL", [EPSILON]),

            Production("PARAMLISTCALL`", ["," , "PARAMLISTCALL"]),
            Production("PARAMLISTCALL`", [EPSILON]),

            Production("PRINTSTAT", ["print", "EXPRESSION"]),

            Production("READSTAT", ["read", "LVALUE"]),

            Production("RETURNSTAT", ["return"]),

            Production("IFSTAT", [type_rule_7, "if", "(", "EXPRESSION", ")", "STATEMENT", "IFSTAT`"]),

            Production("IFSTAT`", [EPSILON]),
            Production("IFSTAT`", ["else", type_rule_8, "STATEMENT"]),

            Production("FORSTAT", [type_rule_9, "for", "(", "ATRIBSTAT", ";", "EXPRESSION", ";", "ATRIBSTAT", ")", break_rule_0, "STATEMENT"]),

            Production("STATELIST", [type_rule_6, break_rule_3, "STATEMENT", "STATELIST`"]),

            Production("STATELIST`", [type_rule_1, break_rule_4, "STATELIST"]),
            Production("STATELIST`", [EPSILON]),

            Production("ALLOCEXPRESSION", ["new", "INTFLOATSTR", "ALLOCEXPRESSION`"]),

            Production("ALLOCEXPRESSION`", ["ALLOCLOOP"]),
            Production("ALLOCEXPRESSION`", [EPSILON]),

            Production("ALLOCLOOP", ["[", "NUMEXPRESSION", "]", "ALLOCLOOP"]),
            Production("ALLOCLOOP", [EPSILON]),

            Production("RELATIONAL", ["<", op_tree_10]),
            Production("RELATIONAL", [">", op_tree_10]),
            Production("RELATIONAL", ["<=", op_tree_10]),
            Production("RELATIONAL", [">=", op_tree_10]),
            Production("RELATIONAL", ["==", op_tree_10]),
            Production("RELATIONAL", ["!=", op_tree_10]),

            Production("EXPRESSION", [type_rule_6, "NUMEXPRESSION", op_tree_7, "EXPRESSION`", op_tree_11]),

            Production("EXPRESSION`", [type_rule_6, "RELATIONAL", "NUMEXPRESSION", op_tree_9]),
            Production("EXPRESSION`", [EPSILON, op_tree_6]),

            Production("NUMEXPRESSION", [type_rule_6, "TERM", op_tree_7, "NUMEXPRESSIONLOOP", op_tree_8]),
            Production("NUMEXPRESSION", [EPSILON, op_tree_6]),

            Production("NUMEXPRESSIONLOOP", [type_rule_14, "+", "TERM", op_tree_4, "NUMEXPRESSIONLOOP", op_tree_5]),
            Production("NUMEXPRESSIONLOOP", [type_rule_14, "-", "TERM", op_tree_4, "NUMEXPRESSIONLOOP", op_tree_5]),
            Production("NUMEXPRESSIONLOOP", [EPSILON, op_tree_6]),

            Production("TERM", [type_rule_6, "UNARYEXPR", op_tree_7, "TERMLOOP", op_tree_8]),

            # Production("TERM`", ["TERMLOOP"]),
            # Production("TERM`", [EPSILON]),

            Production("TERMLOOP", [type_rule_14, "*", "UNARYEXPR", op_tree_4, "TERMLOOP", op_tree_5]),
            Production("TERMLOOP", [type_rule_14, "/", "UNARYEXPR", op_tree_4, "TERMLOOP", op_tree_5]),
            Production("TERMLOOP", [type_rule_14, "%", "UNARYEXPR", op_tree_4, "TERMLOOP", op_tree_5]),
            Production("TERMLOOP", [EPSILON, op_tree_6]),

            Production("UNARYEXPR", [type_rule_13, "+", "FACTOR", op_tree_3]),
            Production("UNARYEXPR", [type_rule_13, "-", "FACTOR", op_tree_3]),
            Production("UNARYEXPR", [type_rule_1, "FACTOR", op_tree_1]),

            Production("FACTOR", ["int_constant", op_tree_0]),
            Production("FACTOR", ["float_constant", op_tree_0]),
            Production("FACTOR", ["string_constant", op_tree_0]),
            Production("FACTOR", ["null", op_tree_0]),
            Production("FACTOR", [type_rule_1, "LVALUE", op_tree_12]),
            Production("FACTOR", ["(", "NUMEXPRESSION", ")", op_tree_13]),

            Production("LVALUE", ["identifier", type_rule_11, op_tree_14, "LVALUE`"]),

            Production("LVALUE`", ["LVALUELOOP"]),
            Production("LVALUE`", ["LVALUEFUNCCALL"]), #
            Production("LVALUE`", [EPSILON]),

            Production("LVALUEFUNCCALL", ["(", "PARAMLISTCALL", ")"]), #
            Production("LVALUELOOP", ["[", "NUMEXPRESSION", "]", "LVALUELOOP"]),
            Production("LVALUELOOP", [EPSILON]),
        ]

        return productions


@dataclass 
class ExprTree:
    name: str
    children: list

    def print_inorder(self):
        print(self.name, end=" ")
        for node in self.children:
            node.print_inorder()

def op_tree_0(parser, origin, target):
    val = target[0]
    origin.syn_expr_tree = ExprTree(val.token.lexema, [])

def op_tree_1(parser, origin, target):
    factor = target[0]
    origin.syn_expr_tree = factor.syn_expr_tree

def op_tree_2(parser, origin, target):
    origin.syn_expr_tree = ExprTree(".", [])

def op_tree_3(parser, origin, target):
    signal = target[0].token.lexema
    factor = target[1]
    origin.syn_expr_tree = ExprTree(".", [
        ExprTree(signal, []),
        factor.syn_expr_tree,
    ])

def op_tree_4(parser, origin, target):
    operator = target[0].token.lexema
    unary_expr = target[1]
    termloop = target[2]

    termloop.her_expr_tree = ExprTree(operator, [
        origin.her_expr_tree,
        unary_expr.syn_expr_tree,
    ])

def op_tree_5(parser, origin, target):
    termloop = target[2]
    origin.syn_expr_tree = termloop.syn_expr_tree

def op_tree_6(parser, origin, target):
    origin.syn_expr_tree = origin.her_expr_tree

def op_tree_7(parser, origin, target):
    unary_expr = target[0]
    termloop = target[1]
    termloop.her_expr_tree = unary_expr.syn_expr_tree

def op_tree_8(parser, origin, target):
    termloop = target[1]
    origin.syn_expr_tree = termloop.syn_expr_tree

def op_tree_9(parser, origin, target):
    relational = target[0]
    num_expr = target[1]
    relational.syn_expr_tree.children.append(origin.her_expr_tree)
    relational.syn_expr_tree.children.append(num_expr.syn_expr_tree)
    origin.syn_expr_tree = relational.syn_expr_tree

def op_tree_10(parser, origin, target):
    operator = target[0].token.lexema
    origin.syn_expr_tree = ExprTree(operator, [])

def op_tree_11(parser, origin, target):
    expression = target[1]
    parser.expression_trees.append(expression.syn_expr_tree)

def op_tree_12(parser, origin, target):
    lvalue = target[0]
    origin.syn_expr_tree = lvalue.syn_expr_tree

def op_tree_13(parser, origin, target):
    numexpression = target[1]
    origin.syn_expr_tree = numexpression.syn_expr_tree

def op_tree_14(parser, origin, target):
    identifier = target[0]
    lvalue_dash = target[1]
    name = identifier.token.lexema
    lvalue_dash.her_expr_tree = ExprTree(name, [])
    origin.syn_expr_tree = lvalue_dash.her_expr_tree

def break_rule_0(parser, origin, target):
    statement = target[8]
    statement.in_loop = True

def break_rule_1(parser, origin, target):
    break_stmt = target[0]
    if not hasattr(origin, "in_loop"):
        origin.in_loop = False
    
    if not origin.in_loop:
        error_info = parser.get_error_info(parser.analyzed_input, break_stmt.token)
        raise CompilaSemanticalError(
            "Break statement outside of a loop.",
            *error_info
        )

def break_rule_2(parser, origin, target):
    statelist = target[6]
    statelist.in_loop = False

def break_rule_3(parser, origin, target):
    statement = target[0]
    statelist = target[1]
    if hasattr(origin, "in_loop"):
        statement.in_loop = origin.in_loop
        statelist.in_loop = origin.in_loop

def break_rule_4(parser, origin, target):
    statelist = target[0]
    if hasattr(origin, "in_loop"):
        statelist.in_loop = origin.in_loop

def break_rule_5(parser, origin, target):
    statelist = target[1]
    if hasattr(origin, "in_loop"):
        statelist.in_loop = origin.in_loop
