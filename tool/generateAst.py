r'''
Description:    This is a script to generate the AST for the Lox interpreter.
                Because of that, it is very scripty and not very classy.
Run:            python generateAst.py C:\Users\esama\Dev\plox\tool
'''
import sys

args = sys.argv

'''
Creates a python file names base_name.py and writes a base class and the extending classes.
'''
def defineAst(output_directory, base_name, list_of_types):
    path = output_directory + '/' + base_name.lower() + '.py'

    f = open(path, 'w')
    lines = [] # the lines we are writing to the file
    lines.append(f'class {base_name}:\n')
    lines.append('    pass\n\n') # for now, pass, since we don't have anything to put in the base class
    
    for _type in list_of_types:
        class_name = _type[0]
        fields = _type[1]
        define_type(lines, base_name, class_name, fields)
    
    f.writelines(lines)
    f.close()


def define_type(lines, base_name, class_name, fields):
    # declare the class extending base_name
    lines.append(f'class {class_name}({base_name}):\n')
    # constructor __init__
    lines.append(f'    def __init__(self, {fields}):\n')
    # split the fields string into a list so we can iterate through each individual field
    fields = fields.split(', ')
    # for each field, self.field = field
    for field in fields:
        lines.append(f'        self.{field} = {field}\n')
    lines.append('\n')


# I want some kind of main function and I know this isn't the same, 
# but I can't think of any other time that this script would be 
# called besides as __main__.
if __name__ == '__main__':
    output_directory = ''
    if len(args) > 2:
        print('Incorrect number of args.\nCorrect usage: python generateAst.py output_directory_here')
        sys.exit(64)
    elif len(args) == 1:
        output_directory = r'C:\Users\esama\Dev\plox'
    else:
        output_directory = args[1]

    defineAst(output_directory, 'Expr', [
        ['Binary', 'expr_left, token_operator, expr_right'],
        ['Grouping', 'expr_expression'],
        ['Literal', 'object_value'],
        ['Unary', 'token_operator, expr_right'],
    ])