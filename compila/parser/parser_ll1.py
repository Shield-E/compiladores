from copy import deepcopy
from functools import partial

from tabulate import tabulate

from compila.constants import END_MARKER, EPSILON
from compila.error import CompilaSyntacticalError
from compila.parser.grammar import Grammar
from compila.parser.tokenizer import Token, Tokenizer


class LL1Table(dict):
    def __str__(self):
        symbols = set()
        tokens = set()

        for symbol, token in self.keys():
            symbols.add(symbol)
            tokens.add(token)

        headers = ["Symbol/Token"] + list(tokens)
        lines = []
        for symbol in symbols:
            line = [symbol]
            for token in tokens:
                key = (symbol, token)
                val = str(self.get(key, ""))
                line.append(val)
            lines.append(line)

        return tabulate(lines, headers=headers, tablefmt="fancy_grid")


class SemanticRule(partial):
    def __repr__(self) -> str:
        return "SemanticRule"


class ParserLL1:
    def __init__(self, tokenizer: Tokenizer, grammar: Grammar):
        self.stacktrace = list()
        self.semantic_on = True
        self.set_tokenizer(tokenizer)
        self.set_grammar(grammar)

    def set_tokenizer(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer

    def set_grammar(self, grammar: Grammar):
        self.grammar = grammar
        self.create_table()

    def analyze(self, string):
        index = 0
        stack = []
        self.stacktrace.clear()

        start_symbol = deepcopy(self.grammar.start_symbol())
        node = start_symbol

        tokens = [i for i in self.tokenizer.run(string)]
        tokens.append(Token(END_MARKER, END_MARKER))
        stack.append(END_MARKER)
        stack.append(start_symbol)

        while len(stack) > 1:
            stacksnapshot = str(stack)
            self.stacktrace.append(stacksnapshot)

            token = tokens[index]
            node = stack.pop()

            if node == EPSILON:
                continue

            if isinstance(node, SemanticRule):
                if self.semantic_on:
                    node()
                continue

            if node == token.name:
                node.token = token
                index += 1
                continue

            if node in self.grammar.terminal:
                raise CompilaSyntacticalError(
                    f'Unexpected node "{node}" found on stack. You may have some error in your grammar'
                )

            if (node, token.name) not in self.table:
                raise CompilaSyntacticalError(
                    f'Unexpected token "{token.name}" found.',
                    'Verify your input code.'
                )

            production = self.table[node, token.name]
            # deepcoping here creates different objects for
            # the same symbol, so it is possible to deal with
            # productions like A -> A + B
            to_stack = [deepcopy(i) for i in production.target]
            avaliable_params = [i for i in to_stack if not callable(i)]

            for i, val in enumerate(to_stack):
                if callable(val):
                    rule = SemanticRule(
                        val,
                        node,
                        *avaliable_params,
                    )
                    to_stack[i] = rule

            # Stacks are FIFO, so we put it in reverse
            stack.extend(reversed(to_stack))

        stacksnapshot = str(stack)
        self.stacktrace.append(stacksnapshot)

        if stack.pop() != END_MARKER:
            raise CompilaSyntacticalError("Something went wrong in the parsing.")

        return start_symbol

    def create_table(self):
        table = LL1Table()

        for production in self.grammar.productions:
            target_symbols = production.get_target_symbols()
            nullable = EPSILON in target_symbols

            if nullable:
                for symbol in self.grammar.follow[production.origin]:
                    table[production.origin, symbol] = production
            else:
                start_symbol = target_symbols[0]
                for symbol in self.grammar.first[start_symbol]:
                    if symbol == EPSILON:
                        continue
                    table[production.origin, symbol] = production

        self.table = table
