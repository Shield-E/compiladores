from collections.abc import Generator

from compila import regexp
from compila.error import CompilaLexicalError
from compila.parser.tokenizer import Token, Tokenizer


class CCLangTokenizer(Tokenizer):
    all_expressions = {
        "identifier"        :r"([a-zA-Z]|_)([a-zA-Z]|[0-9]|_)*",
        "int_constant"      :r"[0-9]+",
        "float_constant"    :r"(-|\+)?[0-9]*.[0-9]+",
        "string_constant"   :r"\"([a-zA-Z]|[0-9]| |_|.|,|:|;|!|0|@|#|$|%|¨|&|/|-|=|{|}|'|[|]|\\)*\"",
        "+"                 :r"\+",
        "-"                 :r"-",
        "*"                 :r"\*",
        "/"                 :r"/",
        "="                 :r"=",
        "=="                :r"==",
        "!="                :r"!=",
        "<"                 :r"<",
        ">"                 :r">",
        "<="                :r"<=",
        ">="                :r">=",
        "("                 :r"\(",
        ")"                 :r"\)",
        "{"                 :r"{",
        "}"                 :r"}",
        "["                 :r"[",
        "]"                 :r"]",
        ","                 :r",",
        ";"                 :r";",
        "_"                 :r" |\n|\t",
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
        "break",
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
                error_hint = self.get_error_info(string, index)
                raise CompilaLexicalError("Invalid expression.", *error_hint)

            yield Token(token_name, lexema=best_match, index=index)

    def get_error_info(self, string:str, index: int):
        RED_COLOR = "\033[31m"
        DISABLE_COLOR = "\033[0m"

        chars = 0
        for i, line in enumerate(string.splitlines()):
            if 0 <= index < chars + len(line):
                break
            # +1 to compensate the newline char
            chars += len(line) + 1

        return (
            f"At line {i + 1}",
            RED_COLOR + line + DISABLE_COLOR,
        )
