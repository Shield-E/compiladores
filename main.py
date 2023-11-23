from compila.regexp.regex_to_automata import compile

machine = compile(r"Hello (World)?")

print(machine.evaluate("Hello"))
print(machine.evaluate("Hello "))
print(machine.evaluate("Hello World"))
print(machine.evaluate("Hello Worlds"))