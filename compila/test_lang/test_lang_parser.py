from compila.parser.grammar import Grammar
from compila.parser.parser_ll1 import ParserLL1
from compila.parser.tokenizer import Tokenizer

from .test_lang_grammar import TestLangGrammar
from .test_lang_tokenizer import TestLangTokenizer


class TestLangParser(ParserLL1):
    def __init__(self):
        tokenizer = TestLangTokenizer()
        grammar = TestLangGrammar()
        super().__init__(tokenizer, grammar)
