from compila.cclang import CCLangParser
from compila.error import CompilaError
from argparse import ArgumentParser

from pathlib import Path


parser = CCLangParser()


def analyze_file(path):
    try:
        path = Path(path)
    except TypeError:
        print("Please provide a valid path!")
        return

    if not path.exists():
        print("File not found!")
        return

    with open(path) as file:
        string = file.read() 

    try:
        parser.analyze(string)
    except CompilaError as error:
        print(f'Error on file "{path}".')
        print(error)
    else:
        for i, tree in enumerate(parser.expression_trees):
            print(f"INORDER FOR EXPRESSION {i}:")
            tree.print_inorder()
            print()

        print("Everything right!")


def main():
    argparser = ArgumentParser(description="Process some integers.")
    argparser.add_argument("-p", "--path", help="path to be analized.")
    argparser.add_argument("-st", "--stacktrace", action='store_true', help="show the stack trace.")

    args = argparser.parse_args()

    analyze_file(args.path)
    
    if args.stacktrace:
        print("STACKTRACE:")
        for trace in parser.stacktrace:
            print(trace)

if __name__ == "__main__":
    main()
