class SymbolTable(dict):
    def add_symbol(self, symbol, _type, _row):
        self[symbol] = _type, _row