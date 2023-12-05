from compila.cclang import CCLangParser
from compila.error import CompilaError
from compila.tac_interpreter import TACInterpreter

from pathlib import Path


parser = CCLangParser()


def analyze_file(path):
    path = Path(path)
    if not path.exists():
        print("Invalid path!")
        return
    
    with open(path) as file:
        string = file.read() 


    try:
        parser.analyze(string)
    except CompilaError as error:
        print(f'Error on file "{path}".')
        print(error)
    else:
        print("Everything right!")


def main():
    analyze_file("example/matrixmult.ccc")


if __name__ == "__main__":
    main()