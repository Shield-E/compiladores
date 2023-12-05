from collections.abc import Generator

from compila import regexp
from compila.error import CompilaLexicalError
from compila.parser.tokenizer import Token, Tokenizer


class CCLangTokenizer(Tokenizer):
    all_expressions = {
        "identifier"    :r"[a-zA-Z]([a-zA-Z]|[0-9])*",
        "int_constant"  :r"[0-9]+",
        "+"             :r"\+",
        "-"             :r"-",
        "*"             :r"\*",
        "/"             :r"/",
        "="             :r"=",
        "=="            :r"==",
        "<"             :r"<",
        ">"             :r">",
        "<="            :r"<=",
        ">="            :r">=",
        "("             :r"\(",
        ")"             :r"\)",
        "{"             :r"{",
        "}"             :r"}",
        "["             :r"[",
        "]"             :r"]",
        ","             :r",",
        ";"             :r";",
        "_"             :r" |\n",
    }

    reserved_words = [
        "def",
        "if",
        "else",
        "for",
        "while",
        "int",
        "float",
        "string",
        "print",
        "read",
        "return",
        "new",
        "null",
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
                yield Token(best_match, best_match, index)
                continue

            if not best_match:
                raise CompilaLexicalError("Invalid expression.")

            yield Token(token_name, lexema=best_match, index=index)
