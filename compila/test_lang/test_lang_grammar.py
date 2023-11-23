from compila.constants import EPSILON
from compila.parser.grammar import Grammar
from compila.parser.production import Production


class TestLangGrammar(Grammar):
    def __init__(self):
        productions = self.create_productions()
        super().__init__(productions)

    def create_productions(self):
        productions = [
            Production("E", ["T", "E'"]),
            Production("E'", ["add", "T", "E'"]),
            Production("E'", ["sub", "T", "E'"]),
            Production("E'", [EPSILON]),

            Production("T", ["F", "T'"]),
            Production("T'", ["mul", "F", "T'"]),
            Production("T'", ["div", "F", "T'"]),
            Production("T'", [EPSILON]),

            Production("F", ["identifier"]),
            Production("F", ["number"]),
            Production("F", ["(", "E", ")"]),
        ]

        return productions
