from sys import argv
from .scanner import lexer
from .parser import parser
from .utils.code_reader import read_source_code


def main():
    print('****************pyva 0.00x**************')
    print('*********Your MiniJava+ compiler********\n')

    try:
        if (len(argv) < 2):
            raise IndexError('No source files specified!')

        raw_source_code = read_source_code(argv[1], 'r')

        print('***************Code read:***************')

        print(raw_source_code)

        print('****************************************\n')
        print('**************Syntax tree:**************')

        parser.parse(raw_source_code, lexer=lexer)

        print('****************************************\n')

    except FileNotFoundError as err:
        print(err)
    except IndexError as err:
        print(err)