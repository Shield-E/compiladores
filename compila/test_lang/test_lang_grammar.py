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


def op_if_code_0(parser, origin, target):
    condition = target[2]
    expression = target[5]    

    origin.syn_code = (
        condition.syn_code
        + 
        f"if t{condition.syn_var} == 0 goto L2:\n"
        +
        expression.syn_code
        +
        "L2:\n"
    )

def op_if_code_1(parser, origin, target):
    number = target[0]
    origin.syn_var = 0
    origin.syn_code = f"t0 = {number.token.lexema} - 5\n"

# Semantic rules to generate code for expressions
def op_expr_code_0(parser, origin, target):
    e = target[0]
    e.her_var = -1
    origin.syn_label = 1
    e.her_code = f"L{origin.syn_label}:\n"

def op_expr_code_1(parser, origin, target):
    e = target[0]
    origin.syn_code = e.syn_code
    origin.syn_var = e.syn_var

def op_expr_code_2(parser, origin, target):
    t = target[0]
    t.her_var = origin.her_var
    t.her_code = origin.her_code

def op_expr_code_3(parser, origin, target):
    identifier = target[0]
    origin.syn_var = origin.her_var + 1
    code = f"t{origin.syn_var} = {identifier.token.lexema}\n"
    origin.syn_code = origin.her_code + code

def op_expr_code_4(parser, origin, target):
    t, e_dash = target
    e_dash.her_var = t.syn_var
    e_dash.her_code = t.syn_code

def op_expr_code_5(parser, origin, target):
    e_dash = target[1]
    origin.syn_var = e_dash.syn_var
    origin.syn_code = e_dash.syn_code

def op_expr_code_6(parser, origin, target):
    t = target[1]
    t.her_var = origin.her_var
    t.her_code = origin.her_code

def op_expr_code_7(parser, origin, target):
    number = target[0]
    origin.syn_var = origin.her_var + 1
    code = f"t{origin.syn_var} = {number.token.lexema}\n"
    origin.syn_code = origin.her_code + code

def op_expr_code_8(parser, origin, target):
    e_dash_1 = target[2]
    origin.syn_var = e_dash_1.syn_var
    origin.syn_code = e_dash_1.syn_code

def op_expr_code_9(parser, origin, target):
    origin.syn_var = origin.her_var
    origin.syn_code = origin.her_code

def op_expr_code_10(parser, origin, target):
    e = target[1]
    e.her_var = origin.her_var
    e.her_code = origin.her_code

def op_expr_code_11(parser, origin, target):
    e = target[1]
    origin.syn_var = e.syn_var
    origin.syn_code = e.syn_code

# 
def op_expr_code_sum(parser, origin, target):
    _, t, e_dash_1 = target
    e_dash_1.her_var = t.syn_var + 1
    code = f"t{e_dash_1.her_var} = t{origin.her_var} + t{t.syn_var}\n"
    e_dash_1.her_code = t.syn_code + code

def op_expr_code_sub(parser, origin, target):
    _, t, e_dash_1 = target
    e_dash_1.her_var = t.syn_var + 1
    code = f"t{e_dash_1.her_var} = t{origin.her_var} - t{t.syn_var}\n"
    e_dash_1.her_code = t.syn_code + code

def op_expr_code_mul(parser, origin, target):
    _, f, t_dash_1 = target
    t_dash_1.her_var = f.syn_var + 1
    code = f"t{t_dash_1.her_var} = t{origin.her_var} * t{f.syn_var}\n"
    t_dash_1.her_code = f.syn_code + code

def op_expr_code_div(parser, origin, target):
    _, f, t_dash_1 = target
    t_dash_1.her_var = f.syn_var + 1
    code = f"t{t_dash_1.her_var} = t{origin.her_var} / t{f.syn_var}\n"
    t_dash_1.her_code = f.syn_code + code
