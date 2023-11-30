from compila.parser.grammar import Grammar
from compila.parser.parser_ll1 import ParserLL1
from compila.parser.tokenizer import Tokenizer

from .cclang_grammar import CCLangGrammar
from .cclang_tokenizer import CCLangTokenizer


class CCLangParser(ParserLL1):
    def __init__(self):
        tokenizer = CCLangTokenizer()
        grammar = CCLangGrammar()
        super().__init__(tokenizer, grammar)
