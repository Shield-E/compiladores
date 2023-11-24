from compila.constants import EPSILON
from compila.parser.grammar import Grammar
from compila.parser.production import Production


class TestLangGrammar(Grammar):
    def __init__(self):
        productions = self.create_productions()
        super().__init__(productions)

    def create_productions(self):
        productions = [
            Production("S", [op_code_0, "E", op_code_1]),
            Production("E", [op_code_2, "T", op_code_4, "E1", op_code_5]),
            Production("E1", ["add", op_code_6, "T", op_code_7, "E1", op_code_8]),
            Production("E1", [EPSILON, op_code_9]),
            Production("T", ["identifier", op_code_3]),
        ]

        return productions

def op_code_0(s, e):
    e.her_var = 0
    e.her_code = ""

def op_code_1(s, e):
    s.syn_code = e.syn_code

def op_code_2(e, t, e_dash):
    t.her_var = e.her_var
    t.her_code = e.her_code

def op_code_3(t, identifier):
    t.syn_var = t.her_var + 1
    code = f"t{t.syn_var} = {identifier.token.lexema}\n"
    t.syn_code = t.her_code + code

def op_code_4(e, t, e_dash):
    e_dash.her_code = t.syn_code
    e_dash.her_var = t.syn_var

def op_code_5(e, t, e_dash):
    e.syn_code = e_dash.syn_code
    e.syn_var = e_dash.syn_var

def op_code_6(e_dash_0, _, t, e_dash_1):
    t.her_code = e_dash_0.her_code
    t.her_var = e_dash_0.her_var

def op_code_7(e_dash_0, _, t, e_dash_1):
    e_dash_1.her_var = t.syn_var + 1
    code = f"t{e_dash_1.her_var} = t{e_dash_0.her_var} + t{t.syn_var}\n"
    e_dash_1.her_code = t.syn_code + code

def op_code_8(e_dash_0, _, t, e_dash_1):
    e_dash_0.syn_code = e_dash_1.syn_code
    e_dash_0.syn_var = e_dash_1.syn_var

def op_code_9(e_dash, _):
    e_dash.syn_code = e_dash.her_code
    e_dash.syn_var = e_dash.her_var
