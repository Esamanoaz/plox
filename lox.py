'''
Title:          Pylox
Description:    A python implementation of the Lox language
Author:         Evan Samano
Start Date:     08/04/2020 MM/DD/YYYY
Recent Date:    07/04/2021 MM/DD/YYYY
'''
import sys

import scanner

num_args = len(sys.argv)
args = sys.argv

class Lox:
    def __init__(self):
        self.had_error = False


    '''
    Run all code at path/to/file.lox
    '''
    def run_file(self, path):
        f = open(path, 'r')
        code = f.read()
        f.close()

        self.run(code)
    
    '''
    Start the REPL
    '''
    def run_prompt(self):
        while True:
            line = input('> ')
            if line == None:
                break

            self.run(line)
            self.had_error = False
    

    '''
    Runs whatever lox code is passed in
    '''
    def run(self, code):
        local_scanner = scanner.Scanner(code) # type(local_scanner) -> Scanner
        tokens = list(local_scanner.scan_tokens())

        for token in tokens:
            print(token)
        
        if self.had_error:
            sys.exit(65)
    

    def error(self, line, where='', message=None):
        self.report(self, line, where, message)
    

    def report(self, line, where, message):
        print(f'[line {line}] Error {where}: {message}')
        self.had_error = True


if __name__ == '__main__':
    x = Lox()
    if num_args > 2:        # If more than just a file path was passed:
        sys.exit(64)
    elif num_args == 2:     # If just a file path was passed:
        x.run_file(args[1])
    else:
        x.run_prompt()        # Else Start the REPL