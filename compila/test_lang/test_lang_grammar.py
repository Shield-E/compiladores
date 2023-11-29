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
            # Production("IF_STMT", [
            #     "if",
            #     "open_parentheses",
            #     "CONDITION",
            #     "close_parentheses",
            #     "open_curly_brackets",
            #     "EXPRESSION",
            #     "close_curly_brackets",
            #     op_if_code_0
            # ]),
            # Production("CONDITION", ["number", op_if_code_1]),

            Production("EXPRESSION", [op_expr_code_start, "E", op_expr_code_end]),

            Production("E", [op_expr_code_0, "T", op_expr_code_1, "E1", op_expr_code_2]),
            Production("E1", ["add", op_expr_code_3, "T", op_expr_code_4, "E1", op_expr_code_add]),
            Production("E1", ["sub", op_expr_code_3, "T", op_expr_code_4, "E1", op_expr_code_sub]),
            Production("E1", [EPSILON, op_expr_code_empty]),

            Production("T", [op_expr_code_0, "F", op_expr_code_1, "T1", op_expr_code_2]),
            Production("T1", ["mul", op_expr_code_3, "F", op_expr_code_4, "T1", op_expr_code_mul]),
            Production("T1", ["div", op_expr_code_3, "F", op_expr_code_4, "T1", op_expr_code_div]),
            Production("T1", [EPSILON, op_expr_code_empty]),

            Production("F", ["identifier", op_expr_code_identifier]),
            Production("F", ["number", op_expr_code_identifier]),
            Production("F", ["open_parentheses", op_expr_code_open_parentheses, "E", op_expr_code_close_parentheses, "close_parentheses"]),
        ]

        return productions


def op_if_code_0(if_stmt, _0, _1, condition, _2, _3, expression, _4):
    if_stmt.syn_code = (
        condition.syn_code
        + 
        f"if t{condition.syn_var} == 0 goto L2:\n"
        +
        expression.syn_code
        +
        "L2:\n"
    )

def op_if_code_1(condition, number):
    condition.syn_var = 0
    condition.syn_code = f"t0 = {number.token.lexema} - 5\n"

# Semantic rules to generate code for expressions
def op_expr_code_start(expression, e):
    e.var_counter = count()

def op_expr_code_end(expression, e):
    expression.code = e.code

def op_expr_code_0(e, t, e_dash):
    t.var_counter = e.var_counter
    e_dash.var_counter = e.var_counter

def op_expr_code_1(e, t, e_dash):
    e_dash.her_var_2 = t.var

def op_expr_code_2(e, t, e_dash):
    e.code = t.code + e_dash.code
    e.var = e_dash.var

def op_expr_code_3(e_dash_0, _, t, e_dash_1):
    t.var_counter = e_dash_0.var_counter
    e_dash_1.var_counter = e_dash_0.var_counter

def op_expr_code_4(e_dash_0, _, t, e_dash_1):
    e_dash_1.her_var_2 = t.var

# 
def op_expr_code_identifier(f, number):
    f.var = f"t{next(f.var_counter)}"
    f.code = f"{f.var} = {number.token.lexema}\n"

def op_expr_code_empty(e_dash, _):
    e_dash.code = ""
    e_dash.var = e_dash.her_var_2

# 
def op_expr_code_number(t, number):
    t.var = f"t{next(t.var_counter)}"
    t.code = f"{t.var} = {number.token.lexema}\n"

def op_expr_code_open_parentheses(f, _0, e, _1):
    e.var_counter - f.var_counter

def op_expr_code_close_parentheses(f, _0, e, _1):
    f.code = e.code
# 
def op_expr_code_add(e_dash_0, _, t, e_dash_1):
    e_dash_0.var = f"t{next(e_dash_0.var_counter)}"
    op_code = f"{e_dash_0.var} = {e_dash_0.her_var_2} + {e_dash_1.var}\n"
    e_dash_0.code = t.code + e_dash_1.code + op_code

def op_expr_code_sub(e_dash_0, _, t, e_dash_1):
    e_dash_0.var = f"t{next(e_dash_0.var_counter)}"
    op_code = f"{e_dash_0.var} = {e_dash_0.her_var_2} - {e_dash_1.var}\n"
    e_dash_0.code = t.code + e_dash_1.code + op_code

def op_expr_code_mul(t_dash_0, _, f, t_dash_1):
    t_dash_0.var = f"t{next(t_dash_0.var_counter)}"
    op_code = f"{t_dash_0.var} = {t_dash_0.her_var_2} * {t_dash_1.var}\n"
    t_dash_0.code = f.code + t_dash_1.code + op_code

def op_expr_code_div(t_dash_0, _, f, t_dash_1):
    t_dash_0.var = f"t{next(t_dash_0.var_counter)}"
    op_code = f"{t_dash_0.var} = {t_dash_0.her_var_2} / {t_dash_1.var}\n"
    t_dash_0.code = f.code + t_dash_1.code + op_code
