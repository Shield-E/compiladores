from compila.constants import EPSILON
from compila.parser.grammar import Grammar
from compila.parser.production import Production
from itertools import count


class TestLangGrammar(Grammar):
    def __init__(self):
        productions = self.create_productions()
        super().__init__(productions)

    def create_productions(self):
        # nota para o futuro:
        # seria bom ter umas funções de gerar a próxima variável
        # ou a próxima label mas elas deveriam ser restritas a cada parser
        # e para cada execução então era bom pensar um pouco sobre como fazer isso
        productions = [
            Production("STATEMENT", [op_statements_0, "ATRIB", op_statements_1]),
            Production("STATEMENT", [op_statements_0, "IF_STMT", op_statements_1]),

            Production("IF_STMT", [
                "if",
                "open_parentheses",
                "CONDITION",
                "close_parentheses",
                "open_curly_brackets",
                "ATRIB",
                "close_curly_brackets",
                "ELSE_STMT",
                op_if,
            ]),

            Production("ELSE_STMT", [
                "else",
                "open_curly_brackets",
                "ATRIB",
                "close_curly_brackets",
                op_else_0,
            ]),
            Production("ELSE_STMT", [EPSILON, op_else_1]),

            Production("ATRIB", ["identifier", "assign", "EXPRESSION", op_assign]),

            Production("CONDITION", [op_cmp_0, "E", op_cmp_1, "CONDITION_1", op_cmp_2]),
            Production("CONDITION_1", ["equal", op_cmp_3, "E", op_cmp_eq]),
            Production("CONDITION_1", ["less_then", op_cmp_3, "E", op_cmp_lt]),
            Production("CONDITION_1", ["greater_then", op_cmp_3, "E", op_cmp_gt]),
            Production("CONDITION_1", ["less_equal", op_cmp_3, "E", op_cmp_le]),
            Production("CONDITION_1", ["greater_equal", op_cmp_3, "E", op_cmp_ge]),
            Production("CONDITION_1", [EPSILON, op_cmp_empty]),

            Production("EXPRESSION", [op_expr_start, "E", op_expr_end]),
            Production("E", [op_expr_0, "T", op_expr_1, "E1", op_expr_2]),
            Production("E1", ["add", op_expr_3, "T", op_expr_4, "E1", op_expr_add]),
            Production("E1", ["sub", op_expr_3, "T", op_expr_4, "E1", op_expr_sub]),
            Production("E1", [EPSILON, op_expr_empty]),
            Production("T", [op_expr_0, "F", op_expr_1, "T1", op_expr_2]),
            Production("T1", ["mul", op_expr_3, "F", op_expr_4, "T1", op_expr_mul]),
            Production("T1", ["div", op_expr_3, "F", op_expr_4, "T1", op_expr_div]),
            Production("T1", [EPSILON, op_expr_empty]),
            Production("F", ["identifier", op_expr_identifier]),
            Production("F", ["number", op_expr_identifier]),
            Production("F", ["open_parentheses", op_expr_open_parentheses, "E", op_expr_close_parentheses, "close_parentheses"]),
        ]

        return productions


class VarCounter:
    def __init__(self, prefix="", suffix=""):
        self.prefix = prefix
        self.suffix = suffix
        self.counter = -1
    
    def next(self):
        self.counter += 1
        return f"{self.prefix}{self.counter}{self.suffix}"


def op_statements_0(parser, origin, target):
    atrib = target[0]
    atrib.label_counter = VarCounter("L")

def op_statements_1(parser, origin, target):
    atrib = target[0]
    origin.code = atrib.code

def op_if(parser, origin, target):
    condition = target[2]
    block = target[5]
    else_stmt = target[7]

    label_false = origin.label_counter.next()
    if_code = f"if false {condition.var} goto {label_false}\n"

    if else_stmt.code:
        label_end = origin.label_counter.next()
        origin.code = (
            condition.code
            + if_code 
            + block.code
            + f"goto {label_end}\n"
            + label_false + ":\n"
            + else_stmt.code 
            + label_end + ":\n"
        )
    else:
        origin.code = (
            condition.code
            + if_code 
            + block.code
            + label_false + ":\n"
        )


def op_else_0(parser, origin, target):
    block = target[2]
    origin.code = block.code

def op_else_1(parser, origin, target):
    origin.code = ""

def op_assign(parser, origin, target):
    identifier, _, expression = target
    origin.var = identifier.token.lexema
    code = f"{origin.var} = {expression.var}\n"
    origin.code = expression.code + code

def op_cmp_0(parser, origin, target):
    expression, condition_1 = target
    var_counter = VarCounter("t")
    expression.var_counter = var_counter
    condition_1.var_counter = var_counter

def op_cmp_1(parser, origin, target):
    expression, condition_1 = target
    condition_1.her_var = expression.var

def op_cmp_2(parser, origin, target):
    expression, condition_1 = target
    origin.code = expression.code + condition_1.code
    origin.var = condition_1.var

def op_cmp_3(parser, origin, target):
    expression = target[1]
    expression.var_counter = origin.var_counter

def op_cmp_eq(parser, origin, target):
    expression = target[1]
    origin.var = origin.var_counter.next()
    origin.code = (
        expression.code 
        + f"{origin.var} = {origin.her_var} == {expression.var}\n"
    )

def op_cmp_lt(parser, origin, target):
    expression = target[1]
    origin.var = origin.var_counter.next()
    origin.code = (
        expression.code 
        + f"{origin.var} = {origin.her_var} < {expression.var}\n"
    )

def op_cmp_gt(parser, origin, target):
    expression = target[1]
    origin.var = origin.var_counter.next()
    origin.code = (
        expression.code 
        + f"{origin.var} = {origin.her_var} > {expression.var}\n"
    )

def op_cmp_le(parser, origin, target):
    expression = target[1]
    origin.var = origin.var_counter.next()
    origin.code = (
        expression.code 
        + f"{origin.var} = {origin.her_var} <= {expression.var}\n"
    )

def op_cmp_ge(parser, origin, target):
    expression = target[1]
    origin.var = origin.var_counter.next()
    origin.code = (
        expression.code 
        + f"{origin.var} = {origin.her_var} >= {expression.var}\n"
    )

def op_cmp_empty(parser, origin, target):
    origin.var = origin.var_counter.next()
    origin.code = f"{origin.var} = {origin.her_var} != 0\n"

# Semantic rules to generate code for expressions
def op_expr_start(parser, origin, target):
    e = target[0]
    e.var_counter = VarCounter("t")

def op_expr_end(parser, origin, target):
    e = target[0]
    origin.code = e.code
    origin.var = e.var

def op_expr_0(parser, origin, target):
    t, e_dash = target
    t.var_counter = origin.var_counter
    e_dash.var_counter = origin.var_counter

def op_expr_1(parser, origin, target):
    t, e_dash = target
    e_dash.her_var = t.var

def op_expr_2(parser, origin, target):
    t, e_dash = target
    origin.code = t.code + e_dash.code
    origin.var = e_dash.var

def op_expr_3(parser, origin, target):
    _, t, e_dash_1 = target
    t.var_counter = origin.var_counter
    e_dash_1.var_counter = origin.var_counter

def op_expr_4(parser, origin, target):
    _, t, e_dash_1 = target
    e_dash_1.her_var = t.var

# 
def op_expr_identifier(parser, origin, target):
    number = target[0]
    origin.var = origin.var_counter.next()
    origin.code = f"{origin.var} = {number.token.lexema}\n"

def op_expr_empty(parser, origin, target):
    origin.code = ""
    origin.var = origin.her_var

# 
def op_expr_number(parser, origin, target):
    number = target[0]
    origin.var = origin.var_counter.next()
    origin.code = f"{origin.var} = {number.token.lexema}\n"

def op_expr_open_parentheses(parser, origin, target):
    e = target[1]
    e.var_counter = origin.var_counter

def op_expr_close_parentheses(parser, origin, target):
    e = target[1]
    origin.code = e.code

# 
def op_expr_add(parser, origin, target):
    _, t, e_dash_1 = target
    origin.var = origin.var_counter.next()
    op_code = f"{origin.var} = {origin.her_var} + {e_dash_1.var}\n"
    origin.code = t.code + e_dash_1.code + op_code

def op_expr_sub(parser, origin, target):
    _, t, e_dash_1 = target
    origin.var = origin.var_counter.next()
    op_code = f"{origin.var} = {origin.her_var} - {e_dash_1.var}\n"
    origin.code = t.code + e_dash_1.code + op_code

def op_expr_mul(parser, origin, target):
    _, f, t_dash_1 = target
    origin.var = origin.var_counter.next()
    op_code = f"{origin.var} = {origin.her_var} * {t_dash_1.var}\n"
    origin.code = f.code + t_dash_1.code + op_code

def op_expr_div(parser, origin, target):
    _, f, t_dash_1 = target
    origin.var = origin.var_counter.next()
    op_code = f"{origin.var} = {origin.her_var} / {t_dash_1.var}\n"
    origin.code = f.code + t_dash_1.code + op_code
