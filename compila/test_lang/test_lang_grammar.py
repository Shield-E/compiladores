from compila.constants import EPSILON
from compila.parser.grammar import Grammar
from compila.parser.production import Production


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
            Production("IF_STMT", [
                "if",
                "open_parentheses",
                "CONDITION",
                "close_parentheses",
                "open_curly_brackets",
                "EXPRESSION",
                "close_curly_brackets",
                op_if_code_0
            ]),
            Production("CONDITION", ["number", op_if_code_1]),

            Production("EXPRESSION", [op_expr_code_0, "E", op_expr_code_1]),

            Production("E", [op_expr_code_2, "T", op_expr_code_4, "E1", op_expr_code_5]),
            Production("E1", ["add", op_expr_code_6, "T", op_expr_code_sum, "E1", op_expr_code_8]),
            Production("E1", ["sub", op_expr_code_6, "T", op_expr_code_sub, "E1", op_expr_code_8]),
            Production("E1", [EPSILON, op_expr_code_9]),

            Production("T", [op_expr_code_2, "F", op_expr_code_4, "T1", op_expr_code_5]),
            Production("T1", ["mul", op_expr_code_6, "F", op_expr_code_mul, "T1", op_expr_code_8]),
            Production("T1", ["div", op_expr_code_6, "F", op_expr_code_div, "T1", op_expr_code_8]),
            Production("T1", [EPSILON, op_expr_code_9]),

            Production("F", ["identifier", op_expr_code_3]),
            Production("F", ["number", op_expr_code_7]),
            Production("F", ["open_parentheses", op_expr_code_10, "E", op_expr_code_11, "close_parentheses"])
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
def op_expr_code_0(expression, e):
    e.her_var = -1
    expression.syn_label = 1
    e.her_code = f"L{expression.syn_label}:\n"

def op_expr_code_1(expression, e):
    expression.syn_code = e.syn_code
    expression.syn_var = e.syn_var

def op_expr_code_2(e, t, e_dash):
    t.her_var = e.her_var
    t.her_code = e.her_code

def op_expr_code_3(t, identifier):
    t.syn_var = t.her_var + 1
    code = f"t{t.syn_var} = {identifier.token.lexema}\n"
    t.syn_code = t.her_code + code

def op_expr_code_4(e, t, e_dash):
    e_dash.her_var = t.syn_var
    e_dash.her_code = t.syn_code

def op_expr_code_5(e, t, e_dash):
    e.syn_var = e_dash.syn_var
    e.syn_code = e_dash.syn_code

def op_expr_code_6(e_dash_0, _, t, e_dash_1):
    t.her_var = e_dash_0.her_var
    t.her_code = e_dash_0.her_code

def op_expr_code_7(t, number):
    t.syn_var = t.her_var + 1
    code = f"t{t.syn_var} = {number.token.lexema}\n"
    t.syn_code = t.her_code + code

def op_expr_code_8(e_dash_0, _, t, e_dash_1):
    e_dash_0.syn_var = e_dash_1.syn_var
    e_dash_0.syn_code = e_dash_1.syn_code

def op_expr_code_9(e_dash, _):
    e_dash.syn_var = e_dash.her_var
    e_dash.syn_code = e_dash.her_code

def op_expr_code_10(f, _0, e, _1):
    e.her_var = f.her_var
    e.her_code = f.her_code

def op_expr_code_11(f, _0, e, _1):
    f.syn_var = e.syn_var
    f.syn_code = e.syn_code

# 
def op_expr_code_sum(e_dash_0, _, t, e_dash_1):
    e_dash_1.her_var = t.syn_var + 1
    code = f"t{e_dash_1.her_var} = t{e_dash_0.her_var} + t{t.syn_var}\n"
    e_dash_1.her_code = t.syn_code + code

def op_expr_code_sub(e_dash_0, _, t, e_dash_1):
    e_dash_1.her_var = t.syn_var + 1
    code = f"t{e_dash_1.her_var} = t{e_dash_0.her_var} - t{t.syn_var}\n"
    e_dash_1.her_code = t.syn_code + code

def op_expr_code_mul(t_dash_0, _, f, t_dash_1):
    t_dash_1.her_var = f.syn_var + 1
    code = f"t{t_dash_1.her_var} = t{t_dash_0.her_var} * t{f.syn_var}\n"
    t_dash_1.her_code = f.syn_code + code

def op_expr_code_div(t_dash_0, _, f, t_dash_1):
    t_dash_1.her_var = f.syn_var + 1
    code = f"t{t_dash_1.her_var} = t{t_dash_0.her_var} / t{f.syn_var}\n"
    t_dash_1.her_code = f.syn_code + code
