from compila.cclang import CCLangParser

parser = CCLangParser()

code = "123 + 456 + 2"

try:
    parser.analyze(code)
except Exception as e:
    print(e)
    for i in parser.stacktrace:
        print(i)
else:
    print("Tudo ocorreu bem")
