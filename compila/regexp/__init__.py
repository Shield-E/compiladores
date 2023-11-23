from .regex_to_automata import compile

def match(expression: str, string: str) -> str:
    """
    Finds the longest portion of the string (from its beginning)
    that still matches the automata language.
    """
    return compile(expression).match(string)

def evaluate(expression: str, string: str) -> bool:
    """
    Checks if the string belongs to the regex language.
    """
    return compile(expression).evaluate(string)
