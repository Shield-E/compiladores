from compila.symbols import EpsilonSymbol, EndMarkerSymbol


DIGITS = "0123456789"
LOWER_CASE = "abcdefghijklmnopqrstuvxwyz"
UPPER_CASE = "ABCDEFGHIJKLMNOPQRSTUVXWYZ"
ALPHANUMERIC = DIGITS + LOWER_CASE + UPPER_CASE

ANY_DIGIT = "|".join(DIGITS)
ANY_LOWER_CASE = "|".join(LOWER_CASE)
ANY_UPPER_CASE = "|".join(UPPER_CASE)
ANY_ALPHANUMERIC = "|".join(ALPHANUMERIC)

EPSILON = EpsilonSymbol()
END_MARKER = EndMarkerSymbol()
