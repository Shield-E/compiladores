class EndMarkerSymbol(str):
    def __repr__(self) -> str:
        return "$"

    def __hash__(self) -> int:
        return hash("EndMarkerSymbol($)")

    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self)

    def __str__(self) -> str:
        return "$"


class EpsilonSymbol(str):
    def __repr__(self) -> str:
        return "Є"

    def __hash__(self) -> int:
        return hash("EpsilonSymbol($)")

    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self)

    def __str__(self) -> str:
        return "Є"


class GrammarSymbol(str):
    def __init__(self, *args, **kwargs):
        str.__init__(*args, **kwargs)
