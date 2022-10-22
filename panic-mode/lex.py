import ply.lex as lex
import sys


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


def main():
    result = ""
    filename = sys.argv[1]

    try:
        file = open(filename)
    except:
        pass

    text = file.read()
    lexer.input(text)
    while True:
        tok = lexer.token()
        if not tok:
            break
        result += str(tok) + "\n"
    with open(filename + ".out", "w") as fo:
        fo.write(result)


if __name__ == "__main__":
    main()
