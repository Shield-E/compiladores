from tabulate import tabulate


class SymbolTable(dict):
    def add_symbol(self, symbol, _type, _row):
        self[symbol] = _type, _row

    def __str__(self):
        headers = ["symbol", "type", "declaration line"]
        data = []

        for key, (_type, _row) in self.items():
            data.append([key, _type, _row])

        return tabulate(data, headers=headers, tablefmt="fancy_grid")
