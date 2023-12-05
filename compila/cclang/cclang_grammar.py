from compila.constants import EPSILON
from compila.parser.grammar import Grammar
from compila.parser.production import Production


class CCLangGrammar(Grammar):
    def __init__(self):
        productions = self.create_productions()
        super().__init__(productions)

    def create_productions(self):
        productions = [
            Production("PROGRAM", ["STATEMENT"]),
            Production("PROGRAM", ["FUNCLIST"]),
            Production("PROGRAM", [EPSILON]),

            Production("FUNCLIST", ["FUNCDEF","FUNCLIST`"]),

            Production("FUNCLIST`", ["[","FUNCLIST","]"]),
            Production("FUNCLIST`", [EPSILON]),

            Production("FUNCDEF", ["def", "identifier", "(", "PARAMLIST", ")", '{', "STATELIST", "}"]),

            Production("INTFLOATSTR", ["int"]),
            Production("INTFLOATSTR", ["float"]),
            Production("INTFLOATSTR", ["str"]),

            Production("PARAMLIST", ["INTFLOATSTR", "PARAMLIST`"]),

            Production("PARAMLIST`", ["identifier", "PARAMLIST``"]),

            Production("PARAMLIST``", ["," , "PARAMLIST"]),
            Production("PARAMLIST``", [EPSILON]),

            Production("STATEMENT", ["VARDECL", ";"]),
            Production("STATEMENT", ["ATRIBSTAT", ";"]),
            Production("STATEMENT", ["PRINTSTAT", ";"]),
            Production("STATEMENT", ["READSTAT", ";"]),
            Production("STATEMENT", ["RETURNSTAT", ";"]),
            Production("STATEMENT", ["IFSTAT"]),
            Production("STATEMENT", ["FORSTAT"]),
            Production("STATEMENT", ["{", "STATELIST", "}"]),
            Production("STATEMENT", ["break", ";"]),
            Production("STATEMENT", [";"]),

            Production("VARDECL", ["INTFLOATSTR", "VARDECL`"]),

            Production("VARDECL`", ["identifier", "VARDECL``"]),
            Production("VARDECL``", ["INTCONSTANTLOOP"]),
            Production("VARDECL``", [EPSILON]),

            Production("INTCONSTANTLOOP", ["[", "int_constant", "]", "INTCONSTANTLOOP`"]),

            Production("INTCONSTANTLOOP`", ["INTCONSTANTLOOP"]),
            Production("INTCONSTANTLOOP`", [EPSILON]),

            Production("ATRIBSTAT", ["LVALUE", "=", "ATRIBSTAT`"]),

            Production("ATRIBSTAT`", ["EXPRESSION"]),
            Production("ATRIBSTAT`", ["ALLOCEXPRESSION"]),
            # Production("ATRIBSTAT`", ["#", "FUNCCALL"]),

            # Production("FUNCCALL", ["identifier", "(", "PARAMLISTCALL", ")"]),

            Production("PARAMLISTCALL", ["identifier", "PARAMLISTCALL`"]),
            Production("PARAMLISTCALL", [EPSILON]),

            Production("PARAMLISTCALL`", ["," , "PARAMLISTCALL"]),
            Production("PARAMLISTCALL`", [EPSILON]),

            Production("PRINTSTAT", ["print", "EXPRESSION"]),

            Production("READSTAT", ["read", "LVALUE"]),

            Production("RETURNSTAT", ["return"]),

            Production("IFSTAT", ["if", "(", "EXPRESSION", ")", "IFSTAT`"]),

            Production("IFSTAT`", ["STATEMENT"]),
            Production("IFSTAT`", ["else", "STATEMENT"]),

            Production("FORSTAT", ["for", "(", "ATRIBSTAT", ";", "EXPRESSION", ";", "ATRIBSTAT", ")", "STATEMENT"]),

            Production("STATELIST", ["STATEMENT", "STATELIST`"]),

            Production("STATELIST`", ["STATELIST"]),
            Production("STATELIST`", [EPSILON]),

            Production("ALLOCEXPRESSION", ["new", "INTFLOATSTR", "ALLOCEXPRESSION`"]),

            Production("ALLOCEXPRESSION`", ["ALLOCLOOP"]),
            Production("ALLOCEXPRESSION`", [EPSILON]),

            Production("ALLOCLOOP", ["[", "NUMEXPRESSION", "]", "ALLOCLOOP"]),
            Production("ALLOCLOOP", [EPSILON]),

            Production("RELATIONAL", ["<", "RELATIONAL`"]),
            Production("RELATIONAL", [">", "RELATIONAL`"]),
            Production("RELATIONAL", ["=="]),
            Production("RELATIONAL", ["!="]),

            Production("RELATIONAL`", ["="]),
            Production("RELATIONAL`", [EPSILON]),

            Production("EXPRESSION", ["NUMEXPRESSION", "EXPRESSION`"]),

            Production("EXPRESSION`", ["RELATIONAL", "NUMEXPRESSION"]),
            Production("EXPRESSION`", [EPSILON]),

            Production("NUMEXPRESSION", ["TERM", "NUMEXPRESSIONLOOP"]),
            Production("NUMEXPRESSION", [EPSILON]),

            Production("NUMEXPRESSIONLOOP", ["+", "TERM", "NUMEXPRESSIONLOOP"]),
            Production("NUMEXPRESSIONLOOP", ["-", "TERM", "NUMEXPRESSIONLOOP"]),
            Production("NUMEXPRESSIONLOOP", [EPSILON]),

            Production("TERM", ["UNARYEXPR", "TERM`"]),

            Production("TERM`", ["TERMLOOP"]),
            Production("TERM`", [EPSILON]),

            Production("TERMLOOP", ["*", "UNARYEXPR", "TERMLOOP"]),
            Production("TERMLOOP", ["/", "UNARYEXPR", "TERMLOOP"]),
            Production("TERMLOOP", ["%", "UNARYEXPR", "TERMLOOP"]),
            Production("TERMLOOP", [EPSILON]),

            Production("UNARYEXPR", ["+", "FACTOR"]),
            Production("UNARYEXPR", ["-", "FACTOR"]),
            Production("UNARYEXPR", ["FACTOR"]),

            Production("FACTOR", ["int_constant"]),
            Production("FACTOR", ["float_constant"]),
            Production("FACTOR", ["string_constant"]),
            Production("FACTOR", ["null"]),
            Production("FACTOR", ["LVALUE"]),
            Production("FACTOR", ["(", "NUMEXPRESSION", ")"]),

            Production("LVALUE", ["identifier", "LVALUE`"]),

            Production("LVALUE`", ["LVALUELOOP"]),
            Production("LVALUE`", ["LVALUEFUNCCALL"]), #
            Production("LVALUE`", [EPSILON]),

            Production("LVALUEFUNCCALL", ["(", "PARAMLISTCALL", ")"]), #
            Production("LVALUELOOP", ["[", "NUMEXPRESSION", "]", "LVALUELOOP"]),
            Production("LVALUELOOP", [EPSILON]),
        ]

        return productions
