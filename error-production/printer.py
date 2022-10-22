from typing import List

class Printer:
    def print_error(self,
                    filename: str,
                    error_msg: str,
                    tokens: list[str],
                    err_token: int):

        """Prints error message in outfile

        Args:
            filename (str): file to write
            error_msg (str): error message
            tokens (list[str]): list of tokens
            err_token (int): index of incorrect token in list
        """        

        with open(filename, "w") as fo:
            fo.write(error_msg + '\n')
            fo.write(" " + " ".join(tokens))
            fo.write('~' * (sum([len(elem) for elem in tokens[:err_token]]) + len(tokens[:err_token])) + '\n')
            fo.write('^' * (len(tokens[err_token]) + 2))
            fo.write('~' * (sum([len(elem) for elem in tokens[err_token + 1:]]) + len(tokens[err_token + 1:])))
    
    def print_condition(self, result, filename: str):

        """Prints the result of parsing in outfile, if it was succesfull

        Args:
            result (Condition): result of parsing presented by a class Condition 
            filename (str): name of outfile
        """   

        with open(filename, "w") as fo:
            fo.write("Bool expression: " + result.bool_expr + '\n')
            fo.write("First branch: " + result.statement + '\n')
            fo.write("Second branch: " + result.else_statement + '\n')