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


def op_statements_0(statements, atrib):
    atrib.label_counter = VarCounter("L")

def op_statements_1(statements, atrib):
    statements.code = atrib.code

def op_if(if_stmt, _0, _1, condition, _2, _3, block, _4, else_stmt):
    label_false = if_stmt.label_counter.next()
    if_code = f"if false {condition.var} goto {label_false}\n"

    if else_stmt.code:
        label_end = if_stmt.label_counter.next()
        if_stmt.code = (
            condition.code
            + if_code 
            + block.code
            + f"goto {label_end}\n"
            + label_false + ":\n"
            + else_stmt.code 
            + label_end + ":\n"
        )
    else:
        if_stmt.code = (
            condition.code
            + if_code 
            + block.code
            + label_false + ":\n"
        )


def op_else_0(else_stmt, _0, _1, block, _2):
    else_stmt.code = block.code

def op_else_1(else_stmt, _):
    else_stmt.code = ""

def op_assign(atrib, identifier, _, expression):
    atrib.var = identifier.token.lexema
    code = f"{atrib.var} = {expression.var}\n"
    atrib.code = expression.code + code

def op_cmp_0(condition, expression, condition_1):
    var_counter = VarCounter("t")
    expression.var_counter = var_counter
    condition_1.var_counter = var_counter

def op_cmp_1(condition, expression, condition_1):
    condition_1.her_var = expression.var

def op_cmp_2(condition, expression, condition_1):
    condition.code = expression.code + condition_1.code
    condition.var = condition_1.var

def op_cmp_3(condition, _, expression):
    expression.var_counter = condition.var_counter

def op_cmp_eq(condition, _, expression):
    condition.var = condition.var_counter.next()
    condition.code = (
        expression.code 
        + f"{condition.var} = {condition.her_var} == {expression.var}\n"
    )

def op_cmp_lt(condition, _, expression):
    condition.var = condition.var_counter.next()
    condition.code = (
        expression.code 
        + f"{condition.var} = {condition.her_var} < {expression.var}\n"
    )

def op_cmp_gt(condition, _, expression):
    condition.var = condition.var_counter.next()
    condition.code = (
        expression.code 
        + f"{condition.var} = {condition.her_var} > {expression.var}\n"
    )

def op_cmp_le(condition, _, expression):
    condition.var = condition.var_counter.next()
    condition.code = (
        expression.code 
        + f"{condition.var} = {condition.her_var} <= {expression.var}\n"
    )

def op_cmp_ge(condition, _, expression):
    condition.var = condition.var_counter.next()
    condition.code = (
        expression.code 
        + f"{condition.var} = {condition.her_var} >= {expression.var}\n"
    )

def op_cmp_empty(condition, _):
    condition.var = condition.var_counter.next()
    condition.code = f"{condition.var} = {condition.her_var} != 0\n"

# Semantic rules to generate code for expressions
def op_expr_start(expression, e):
    e.var_counter = VarCounter("t")

def op_expr_end(expression, e):
    expression.code = e.code
    expression.var = e.var

def op_expr_0(e, t, e_dash):
    t.var_counter = e.var_counter
    e_dash.var_counter = e.var_counter

def op_expr_1(e, t, e_dash):
    e_dash.her_var = t.var

def op_expr_2(e, t, e_dash):
    e.code = t.code + e_dash.code
    e.var = e_dash.var

def op_expr_3(e_dash_0, _, t, e_dash_1):
    t.var_counter = e_dash_0.var_counter
    e_dash_1.var_counter = e_dash_0.var_counter

def op_expr_4(e_dash_0, _, t, e_dash_1):
    e_dash_1.her_var = t.var

# 
def op_expr_identifier(f, number):
    f.var = f.var_counter.next()
    f.code = f"{f.var} = {number.token.lexema}\n"

def op_expr_empty(e_dash, _):
    e_dash.code = ""
    e_dash.var = e_dash.her_var

# 
def op_expr_number(t, number):
    t.var = t.var_counter.next()
    t.code = f"{t.var} = {number.token.lexema}\n"

def op_expr_open_parentheses(f, _0, e, _1):
    e.var_counter = f.var_counter

def op_expr_close_parentheses(f, _0, e, _1):
    f.code = e.code

# 
def op_expr_add(e_dash_0, _, t, e_dash_1):
    e_dash_0.var = e_dash_0.var_counter.next()
    op_code = f"{e_dash_0.var} = {e_dash_0.her_var} + {e_dash_1.var}\n"
    e_dash_0.code = t.code + e_dash_1.code + op_code

def op_expr_sub(e_dash_0, _, t, e_dash_1):
    e_dash_0.var = e_dash_0.var_counter.next()
    op_code = f"{e_dash_0.var} = {e_dash_0.her_var} - {e_dash_1.var}\n"
    e_dash_0.code = t.code + e_dash_1.code + op_code

def op_expr_mul(t_dash_0, _, f, t_dash_1):
    t_dash_0.var = t_dash_0.var_counter.next()
    op_code = f"{t_dash_0.var} = {t_dash_0.her_var} * {t_dash_1.var}\n"
    t_dash_0.code = f.code + t_dash_1.code + op_code

def op_expr_div(t_dash_0, _, f, t_dash_1):
    t_dash_0.var = t_dash_0.var_counter.next()
    op_code = f"{t_dash_0.var} = {t_dash_0.her_var} / {t_dash_1.var}\n"
    t_dash_0.code = f.code + t_dash_1.code + op_code
