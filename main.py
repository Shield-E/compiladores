from compila.test_lang import TestLangParser

parser = TestLangParser()

code = "123 + hello * 2"

try:
    parser.analyze(code)
except Exception as e:
    print(e)
    for i in parser.stacktrace:
        print(i)
else:
    print("Tudo ocorreu bem")
