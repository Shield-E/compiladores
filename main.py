from compila.test_lang import TestLangParser
from compila.error import CompilaError
from compila.tac_interpreter import TACInterpreter

parser = TestLangParser()

origin_code = "a + 1"

bla = parser.analyze(origin_code)

tac_code = (
    "a = 0\n" 
    +
    bla.syn_code 
    +
    "a = t2\n"
    "print a\n"
    "if a < 5 goto L1:\n"
)
print(tac_code)

interpreter = TACInterpreter()
interpreter.run(tac_code)
