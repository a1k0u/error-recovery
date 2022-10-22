import ply.lex as lex
import sys

reserved = {
    "if": "IF",
    "then": "THEN",
    "else": "ELSE"
}

tokens = [
             'ID',
             'EQ',
             'EPS',
             'ASSIGN',
             'SEMICOLON'
         ] + list(reserved.values())


def t_ID(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, "ID")
    return t


t_SEMICOLON = r'\;'
t_ASSIGN = r'\='
t_EQ = r'\=\='

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