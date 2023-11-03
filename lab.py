tabela = {
    ('S', '0M'): ['B'],
    ('S', '1M'): ['B'],
    ('S', '0'): ['B'],
    ('S', '1'): ['B'],

    ('B', '0M'): ['0M', 'Bl'],
    ('B', '1M'): ['1M', 'Bl'],
    ('B', '0'): ['0'],
    ('B', '1'): ['1'],

    ('Bl', '0m'): ['Om','B'],
    ('Bl', '1m'): ['1m', 'B'],
    ('Bl', '0'): ['0'],
    ('Bl', '1'): ['1'],
}
tabela_regras = {
    ('S', '0M'): ['B'],
    ('S', '1M'): ['B'],
    ('S', '0'): ['B'],
    ('S', '1'): ['B'],

    ('B', '0M'): ['0M', 'Bl'],
    ('B', '1M'): ['1M', 'Bl'],
    ('B', '0'): ['0'],
    ('B', '1'): ['1'],

    ('Bl', '0m'): ['Om', 'B'],
    ('Bl', '1m'): ['1m', 'B'],
    ('Bl', '0'): ['0'],
    ('Bl', '1'): ['1'],
}
memoria_regras = {
    'Bl.val': 0,
    'B.val': 0,
    'Bl.lvl': 0,
    'B.lvl': 0,
    'S.val': 0,
}
terminal = {'0M','1m','0m','1M','0','1'}
naoterminal = {'S', 'B', 'Bl'}
w = ['0M','1m','1M','0']
ip = 0
stack = []
stack.append('$')
stack.append('S')
x = stack[-1]

while x != '$':
    if x == w[ip]:
        stack.pop()
        x = stack[-1]
        ip = ip + 1
        continue
    if x in terminal:
        print('deu merda')
        break
    if (x, w[ip]) not in tabela:
        print('deu merda 1')
        break

    stack.pop()
    stack.extend(reversed(tabela[x,w[ip]]))
    x = stack[-1]
    print(stack)

def executa_regra(rule):
    for key in memoria_regras:
        rule = rule.replace(key, f'memoria_regras["{key}"]')
        exec(rule)