import ply.yacc as yacc

import sys
import os
from typing import List
from lex import tokens
from lex import TokenError

LINES: List[str] = []
VARIABLES = {}


class ParserError(Exception):
    pass


def p_output(p):
    """
    output : OUT VAR SEMICOLON
    """

    variable_value = VARIABLES.get(p[2], 0)
    print(variable_value)

    p[0] = variable_value


def p_variable(p):
    """
    output : VAR ASSIGN expression SEMICOLON
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


def p_error(p):
    if p is None:
        raise ParserError("Syntax error: Unexpected end of file ...")

    token = f"{p.type}({p.value}) on line {p.lineno}"
    raise ParserError(f"Syntax error: Unexpected {token}")


PARSER = yacc.yacc()


def main():
    if len(sys.argv) == 1:
        exit("Args error: Waiting your file ...")

    if not os.path.exists(sys.argv[1]):
        exit("Args error: File not found ...")

    file_path = os.path.abspath(sys.argv[1])

    with open(file_path, "r", encoding="utf-8") as code_in, open(
        f"{file_path}.stdout", "w"
    ) as code_out:
        for line in code_in.readlines():
            PARSER.parse(line)

            """
            LINES.append(line.rstrip())

            try:
                result = PARSER.parse(LINES[-1])
                while not result:
                    result = PARSER.parse(LINES[-1])
            except (ParserError, TokenError) as e:
                exit(*e.args)"""

        # code_out.writelines(LINES)

    print("File is processed ...")


if __name__ == "__main__":
    main()
