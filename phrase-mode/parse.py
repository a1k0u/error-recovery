import io

import ply.yacc as yacc

import sys
import os
from typing import List
from lex import tokens
from lex import TokenError

LINES: List[str] = []
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

    if len(p) == 5:
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
    p[0] = not None


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


def p_error(p):

    if p is None:
        raise ParserError(
            __correct_line("error: Unexpected end of file", f"{LINES[-1]};")
        )

    print(p)

    raise ParserError(
        __correct_line("error: incorrect output", "OUT -1;")
    )


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
        global STDERR_FILE

        STDERR_FILE = code_err

        for line in code_in.readlines():
            LINES.append(line.rstrip())

            result = None
            while result is None:
                try:
                    result = PARSER.parse(LINES[-1])
                except ParserError:
                    continue

        code_out.write("\n".join(LINES))

    print("File is processed ...")


if __name__ == "__main__":
    main()
