from compila.test_lang import TestLangParser
from compila.error import CompilaError
from compila.tac_interpreter import TACInterpreter

parser = TestLangParser()

origin_code = "if (123 < 1234) {bla = 5 + 2} else {bla = 5 - 2}"

bla = parser.analyze(origin_code)
inter_code = bla.code + "print bla"

print(inter_code)
print()

# interpreter = TACInterpreter()
# interpreter.run(inter_code)
