import sys
from typing import List

import ply.yacc as yacc
 
from lex import tokens
from printer import Printer

ERROR_MSG = {
    ";": "Found unexpected semicolon before else"
}

class Condition:
    def __init__(self, bool_expr: str, statement: str, else_statement: str):
        self.bool_expr = bool_expr
        self.statement = statement
        self.else_statement = else_statement
        self.exit_code = 0

class Error:
    def __init__(self):
        self.exit_code = 1

def p_if_statement(p):
    '''
    if_statement : IF bool_expr THEN statement else_part
    '''
    if (any([token is None for token in [p[1], p[2], p[3], p[4], p[5]]])):
        p[0] = Error()
        return
    p[0] = Condition(p[2], p[4], p[5])
    
def p_start(p):
    '''
    bool_expr : ID EQ ID
    '''
    p[0] = " ".join([p[1], p[2], p[3]])

def p_statement(p):
    '''
    statement : ID ASSIGN ID
    '''
    p[0] = " ".join([p[1], p[2], p[3]])

def p_else_part(p):
    '''
    else_part :      ELSE statement SEMICOLON
                   | empty
                   | SEMICOLON ELSE statement SEMICOLON
    '''
    if (len(p) == 5):
        printer.print_error(outfile, ERROR_MSG[p[1]], [p[1], p[2], p[3], p[4]], 0)
        return
    if (len(p) == 2):
        return
    p[0] = p[2]

def p_empty(p):
     'empty :'
     pass

def p_error(p):
    print("Error")

printer = Printer()
outfile = str()

def main():
    parser = yacc.yacc()
 
    filename = sys.argv[1]
    try:
        file = open(filename)
    except OSError:
        print("Unable to open file: ", filename)
        return

    text = file.read()
    result = parser.parse(text)
    print(result)
    if result.exit_code == 1:
        return
    printer.print_condition(result, outfile)

if __name__ == "__main__":
    outfile = sys.argv[1] + ".out"
    main()
    