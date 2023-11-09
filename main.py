import ply.lex as lex
# todo: adicionar palavras reservadas
reserved = {
    'def': 'DEF',
    'int': 'INT_DECL',
    'float': 'FLOAT_DECL',
    'string': 'STRING_DECL',
    'print': 'PRINT',
    'read': 'READ',
    'return': 'RETURN',
    'if': 'IF',
    'for': 'FOR',
    'new': 'NEW'
}
# todo: adicionar lista dos nomes dos tokens

# todo: adicionar regras com expressoes regulares para identificação de tokens

# todo: adicionar funcoes de achar linhas e colunas

# todo: adicionar regra para ignorar espacos e tabs

# todo : adicionar regra para tratar erros lexicos

# todo: ler arquivo txt dos dados

# todo: percorrer o arquivo, ler os tokens, e preencher a tabela de simbolos