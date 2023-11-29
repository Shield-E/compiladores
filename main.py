from compila.test_lang import TestLangParser
from compila.error import CompilaError
from compila.tac_interpreter import TACInterpreter

parser = TestLangParser()

origin_code = "if (blin == blon) {bla = 5 + 5 - 2} else {foo = 123 - b}"
# origin_code = "hello = a + b * c + d / 2"

bla = parser.analyze(origin_code)
# inter_code = bla.syn_code + "print t0"
print(bla.code)

# print(inter_code)

# interpreter = TACInterpreter()
# interpreter.run(inter_code)
