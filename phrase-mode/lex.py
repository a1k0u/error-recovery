"""
Lexer for plus-expression-variables-out language.

Example:
    a = 1;
    c = 1 + 2 + 3;
    b = a + 1;

    OUT b;
"""

import ply
import os
import sys


class TokenError(Exception):
    pass


LEXER = ply.lex.lex()

reserved = {
    "out": "OUT"
}

tokens = [
    "VAR",
    "NUM",
    "ASSIGN",
    "SEMICOLON",
    "PLUS",
    *reserved.values()
]

t_PLUS = r"\+"
t_ASSIGN = r"\="
t_SEMICOLON = r"\;"


def t_VAR(t: ply.lex.LexToken):
    r"""[a-zA-Z][0-9a-zA-Z_]*"""
    t.type = reserved.get(t.value, "VAR")
    return t


def t_NUM(t: ply.lex.LexToken):
    r"""[0-9]+"""
    t.value = int(t.value)


def t_newline(t: ply.lex.LexToken):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_error(t: ply.lex.LexToken):
    raise TokenError(
        f"Syntax error: Illegal character '{t.value[0]}'."
    )


def main():
    if len(sys.argv) == 1:
        exit("Waiting your file ...")

    if not os.path.exists(sys.argv[1]):
        exit("File not found ...")

    file_path = os.path.abspath(sys.argv[1])

    with open(file_path, "r", encoding="utf-8") as read_lang, open(
        file_path + ".out", "w"
    ) as write_lang:
        for line in read_lang.readlines():
            LEXER.input(line.rstrip())

            while True:
                try:
                    token = LEXER.token()
                except TokenError as e:
                    exit(*e.args)

                if not token:
                    break

                print(token, file=write_lang)

    print("File is processed ...")


if __name__ == "__main__":
    main()
