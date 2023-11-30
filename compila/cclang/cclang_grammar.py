from compila.constants import EPSILON
from compila.parser.grammar import Grammar
from compila.parser.production import Production


class CCLangGrammar(Grammar):
    def __init__(self):
        productions = self.create_productions()
        super().__init__(productions)

    def create_productions(self):
        productions = [
            Production("E", ["T", "E1"]),
            Production("E1", ["add", "T", "E1"]),
            Production("E1", [EPSILON]),
            Production("T", ["number"]),
        ]

        return productions
