import sys
from typing import List

from lex import lex
from printer import Printer


class VPParser:
    def __init__(self):
        self.ans = ""
        self.error_code = 0

    def parse(self, tokens) -> str:
        stack = []
        for tok in tokens:
            if tok.type == 'OPENING':
                stack.append(tok)
            elif tok.type == 'CLOSING':
                if len(stack) == 0:
                    printer.print_error('log.txt', tokens, 'Unexpected closing bracket', tok.lexpos)
                    self.error_code = 1
                else:
                    stack.pop()
            self.ans += tok.value

        if len(stack) != 0:
            while len(stack) != 0:
                tok = stack.pop()
                printer.print_error('log.txt', tokens, 'Opening bracket is not closed', tok.lexpos)
                self.error_code = 2
        return self.ans


printer = Printer()
outfile = str()


def main():
    filename = sys.argv[1]
    try:
        file = open(filename)
    except OSError:
        print("Unable to open file: ", filename)
        return

    text = file.read()
    tokens = lex(text)
    parser = VPParser()
    result = parser.parse(tokens)

    if parser.error_code == 0:
        printer.print_condition(result, outfile)


if __name__ == "__main__":
    outfile = sys.argv[1] + ".out"
    main()
