"""
    Language for testing phrase
    mode error recovery strategy.

    There is a code which have errors: miss semicolons,
                                       miss operation,
                                       expected plus, but got assign,
                                       and their combination:
        OUT 5 1 + aba = 1033 + 1

        a = b + 1 + c + 10
        k = a b c d + 10 + 2 5 + 1
        b = 10; OUT b; b = 20; OUT b

        OUT a

    It will transform into:
        OUT 5 + 1 + aba  +  1033 + 1;
        
        a = b + 1 + c + 10;
        k = a + b + c + d + 10 + 2 + 5 + 1;
        b = 10; OUT b; b = 20; OUT b;

        OUT a;
"""

import ply.yacc as yacc

import sys
import os
from typing import List

from lex import tokens
from lex import lexer

LINES: List[str] = []
FIX_OPERATOR = False
STDERR_FILE = None
VARIABLES = {}


class ParserError(Exception):
    pass


def __correct_line(warning_message: str, correct_code: str) -> str:
    STDERR_FILE.write(f"{warning_message} at {len(LINES)} line.\n")
    LINES[-1] = correct_code
    return warning_message


def p_output(p):
    """
    operation : OUT object SEMICOLON operation
              | object SEMICOLON operation
              | empty
    """

    if len(p) == 5 and p[2] is not None:
        print(p[2])

    p[0] = not None


def p_object(p):
    """
    object : variable
           | expression
           | empty
    """

    p[0] = p[1]


def p_variable(p):
    """
    variable : VAR ASSIGN expression
    """

    VARIABLES[p[1]] = p[3]
    p[0] = p[3]


def p_expression_plus(p):
    """
    expression : expression PLUS expression
    """

    p[0] = p[1] + p[3]


def p_expression_literal(p):
    """
    expression : NUM
    """

    p[0] = p[1]


def p_expression_variable(p):
    """
    expression : VAR
    """

    p[0] = VARIABLES.get(p[1], 0)


def p_empty(_):
    """empty :"""

    pass


def p_error_expression(p):
    """
    expression : expression expression
    """

    global FIX_OPERATOR

    p[0] = p[1] + p[2]

    lexer.input(LINES[-1])

    token_prev = lexer.token()
    while True:
        token_new = lexer.token()

        if token_prev.type in ("NUM", "VAR") and token_new.type in ("NUM", "VAR"):
            st1, fn1 = token_prev.lexpos, len(str(token_prev.value))
            st2, fn2 = token_new.lexpos, len(str(token_new.value))
            break

        token_prev, token_new = token_new, None

    c = LINES[-1]
    __correct_line(
        "warning: expected plus in expression",
        f"{c[: st1]}{c[st1 : st1 + fn1]} + {c[st2 : st2 + fn2]}{c[st2 + fn2 :]}",
    )

    FIX_OPERATOR = True


def p_error(p):
    if p is None:
        raise ParserError(__correct_line("warning: expected ';'", f"{LINES[-1]};"))

    if FIX_OPERATOR:
        raise ParserError

    if p.type == "ASSIGN":
        p.type = "PLUS"
        p.value = "+"

        c = LINES[-1]
        raise ParserError(
            __correct_line(
                "warning: expected plus, got assign",
                f"{c[:p.lexpos]} + {c[p.lexpos + 1:]}",
            )
        )

    raise ParserError(__correct_line("warning: incorrect output", "OUT -1;"))


PARSER = yacc.yacc()


def main():
    if len(sys.argv) == 1:
        exit("Args error: Waiting your file ...")

    if not os.path.exists(sys.argv[1]):
        exit("Args error: File not found ...")

    file_path = os.path.abspath(sys.argv[1])

    with open(file_path, "r", encoding="utf-8") as code_in, open(
        f"{file_path}.stdout", "w"
    ) as code_out, open(f"{file_path}.stderr", "w") as code_err:
        global STDERR_FILE, FIX_OPERATOR

        STDERR_FILE = code_err

        for line in code_in.readlines():
            LINES.append(line.rstrip())

            FIX_OPERATOR = False

            result = None
            while result is None:
                try:
                    result = PARSER.parse(LINES[-1])
                except ParserError:
                    continue

        code_out.write("\n".join(LINES))


if __name__ == "__main__":
    main()
