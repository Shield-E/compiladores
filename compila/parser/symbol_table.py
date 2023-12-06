class SymbolTable(dict):
    def add_symbol(self, symbol, _type, _scope):
        self[symbol] = _type