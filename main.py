from compila.test_lang import TestLangParser
from compila.error import CompilaError


parser = TestLangParser()

code = "123 + hello ** 2"

try:
    parser.analyze(code)
except CompilaError as error:
    print(error)
else:
    print("Tudo ocorreu bem")
