FILE?=example/djikstra.ccc

run:
	python3 main.py -p $(FILE) | tee output.txt

install:
	pip install treelib
	pip install tabulate
