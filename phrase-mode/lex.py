"""
Lexer for plus-expression-variables-out language.

Example:
    a = 1;
    c = 1 + 2 + 3;
    b = a + 1;

    OUT b;
"""

import ply.lex as lex
import os
import sys


class TokenError(Exception):
    pass


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

t_ignore = r" "


def t_VAR(t: lex.LexToken):
    r"""[a-zA-Z][0-9a-zA-Z_]*"""
    if t.value == "OUT":
        t.type = "OUT"
    else:
        t.type = "VAR"
    return t


def t_NUM(t: lex.LexToken):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_newline(t: lex.LexToken):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_error(t: lex.LexToken):
    raise TokenError(
        f"Syntax error: Illegal character '{t.value[0]}'."
    )


lexer = lex.lex()
