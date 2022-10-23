import ply.lex as lex

tokens = [
    'OPENING',
    'CLOSING'
]

t_OPENING = r'\('
t_CLOSING = r'\)'
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def lex(text) -> list:
    result = []
    lexer.input(text)
    while True:
        tok = lexer.token()
        if not tok:
            break
        result.append(tok)
    return result
