from collections.abc import Generator

from compila import regexp
from compila.error import CompilaLexicalError
from compila.parser.tokenizer import Token, Tokenizer


class TestLangTokenizer(Tokenizer):
    all_expressions = dict(
        identifier=r"[a-zA-Z]([a-zA-Z]|[0-9])*",
        number=r"[0-9]+",
        add=r"\+",
        sub=r"-",
        mul=r"\*",
        div=r"/",
        assign=r"=",
        equal=r"==",
        open_parentheses=r"\(",
        close_parentheses=r"\)",
        open_curly_brackets=r"{",
        close_curly_brackets=r"}",
        _=r" ",
    )

    reserved_words = [
        "if",
        "else",
        "for",
        "while",
    ]

    def run(self, string: str) -> Generator[Token]:
        all_machines = {
            name: regexp.compile(exp) for name, exp in self.all_expressions.items()
        }

        index = 0
        while index < len(string):
            token_name = ""
            best_match = ""
            substring = string[index:]

            for name, machine in all_machines.items():
                current_match = machine.match(substring)
                if len(current_match) > len(best_match):
                    token_name = name
                    best_match = current_match
            index += len(best_match)

            if token_name == "_":
                continue
            
            if (token_name == "identifier") and (best_match in self.reserved_words):
                yield Token(best_match, best_match)
                continue

            if not best_match:
                raise CompilaLexicalError("Invalid expression.")

            yield Token(token_name, lexema=best_match)
