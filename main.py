from compila.test_lang import TestLangParser
from compila.error import CompilaError
from compila.tac_interpreter import TACInterpreter

parser = TestLangParser()

origin_code = "if (2) {5 + 5 - 2}"
# origin_code = "2 + 3 * 5"

bla = parser.analyze(origin_code)
inter_code = bla.syn_code + "print t0"
print(inter_code)

interpreter = TACInterpreter()
interpreter.run(inter_code)
