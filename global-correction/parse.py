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
                    pass
                else:
                    self.ans += tok.value
            self.ans += tok.value

        for _ in range(len(stack)):
            self.ans += ')'
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
