'''
Title:          Pylox
Description:    A python implementation of the Lox language
Author:         Evan Samano
Start Date:     08/04/2020 MM/DD/YYYY
Recent Date:    07/04/2021 MM/DD/YYYY
'''
import sys

from scanner import Scanner

num_args = len(sys.argv)
args = sys.argv

class Lox:
    def __init__(self):
        if num_args > 2:        # If more than just a file path was passed:
            sys.exit(64)
        elif num_args == 1:     # If just a file path was passed: #if something doesnt work try changing 1 to 2
            run_file(args[1])
        else:
            run_prompt()        # Else Start the REPL
        
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
        scanner = Scanner(code)
        tokens = list(scanner.scan_tokens())

        for token in tokens:
            print(token)
        
        if had_error:
            sys.exit(65)
    

    def error(self, line, where, message):
        report(line, where, message) #report(data, line, where, message)
    

    def report(self, line, where, message):
        print(f'[line {line}] Error {where}: {message}')
        self.had_error = True
