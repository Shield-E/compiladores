from compila.symbols import GrammarSymbol, EpsilonSymbol, EndMarkerSymbol


class Production:
    def __init__(self, origin: str, target: str | tuple[str]):
        self.origin = GrammarSymbol(origin)
        self.target = self._fix_target_types(target)

    def get_target_symbols(self):
        return [i for i in self.target if not callable(i)]

    def get_non_empty_symbols(self):
        return [i for i in self.get_target_symbols() 
                if not isinstance(i, (EpsilonSymbol, EndMarkerSymbol))]

    def _fix_target_types(self, target):
        new_target = []
        for data in target:
            if callable(data):
                new_target.append(data)
            elif isinstance(data, (EpsilonSymbol, EndMarkerSymbol)):
                new_target.append(data)
            else:
                new_target.append(GrammarSymbol(data))
        return tuple(new_target)

    def __str__(self) -> str:
        targets = " ".join(str(i) for i in self.get_target_symbols())
        return f"{self.origin} → {targets}"
