from collections.abc import Generator
from dataclasses import dataclass


@dataclass
class Token:
    name: str
    lexema: str
    index: int = 0


class Tokenizer:
    def run(self, string: str) -> Generator[Token]:
        for i in string:
            yield Token("char", i)
