
class Printer:
    @staticmethod
    def print_error(filename: str,
                    tokens: list,
                    error_msg: str,
                    lex_pos: int) -> None:

        """Prints error message in outfile
        Args:
            filename (str): file to write
            tokens (list): tokens
            error_msg (str): error message
            lex_pos (int): index of incorrect token in list
        """
        with open(filename, "a") as fo:
            fo.write(error_msg + '\n')
            for tok in tokens:
                fo.write(tok.value)
            fo.write('\n')
            for i in range(len(tokens)):
                if i == lex_pos:
                    fo.write('^')
                else:
                    fo.write('~')
            fo.write('\n')

    @staticmethod
    def print_condition(result, filename: str) -> None:
        """Prints the result of parsing in outfile, if it was succesful

        Args:
            result (Condition): result of parsing presented by a class Condition
            filename (str): name of outfile
        """

        with open(filename, "w") as fo:
            fo.write(result)
