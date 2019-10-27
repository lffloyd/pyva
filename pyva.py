from sys import argv
from src.scanner import lexer
from src.parser import parser
from src.utils.code_reader import read_source_code

print('****************pyva 0.00x**************')
print('*********Your MiniJava+ compiler********')

try:
    if (len(argv) < 2):
        raise IndexError('No source files specified!')

    raw_source_code = read_source_code(argv[1], 'r')

    print('***************Code read:***************')

    print(raw_source_code)

    parser.parse(raw_source_code, lexer=lexer)

except FileNotFoundError as err:
    print(err)
except IndexError as err:
    print(err)