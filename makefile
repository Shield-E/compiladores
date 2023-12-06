FILE?=example/djikstra.ccc

run:
	python3 main.py -p $(FILE)

install:
	pip install treelib
	pip install tabulate
