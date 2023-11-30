class CompilaError(Exception):
    def __str__(self) -> str:
        name = self.__class__.__name__
        message = "\n\t".join(self.args)
        return f"{name}:\n\t{message}"


class CompilaLexicalError(CompilaError):
    pass


class CompilaSyntacticalError(CompilaError):
    pass
