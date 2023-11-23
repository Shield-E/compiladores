from compila.parser.tokenizer import Token, Tokenizer
from compila.constants import ANY_DIGIT, ANY_LOWER_CASE, ANY_UPPER_CASE

from collections.abc import Generator


class RegexTokenizer(Tokenizer):
    simplifications = {
        "[0-9]": f"({ANY_DIGIT})",
        "[a-z]": f"({ANY_LOWER_CASE})",
        "[A-Z]": f"({ANY_UPPER_CASE})",
        "[a-Z]": f"({ANY_LOWER_CASE}|{ANY_UPPER_CASE})",
        "[a-zA-Z]": f"({ANY_LOWER_CASE}|{ANY_UPPER_CASE})",
    }

    def run(self, string: str) -> Generator[Token]:
        for shortcut, replacement in self.simplifications.items():
            string = string.replace(shortcut, replacement)

        for i in string:
            yield Token(name=i, lexema=i)
