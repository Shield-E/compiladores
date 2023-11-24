from compila.test_lang import TestLangParser
from compila.error import CompilaError

parser = TestLangParser()

code = "a + b + c"
bla = parser.analyze(code)

print(bla.syn_code)
