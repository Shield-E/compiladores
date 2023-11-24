from compila.test_lang import TestLangParser
from compila.error import CompilaError
from compila.tac_interpreter import TACInterpreter

parser = TestLangParser()

origin_code = "2 + 3 * 8 - 5"
bla = parser.analyze(origin_code)

tac_code = bla.syn_code

interpreter = TACInterpreter()
interpreter.run(tac_code)
