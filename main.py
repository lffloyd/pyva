from src.scanner import lexer
from src.parser import parser
from src.utils.code_reader import read_source_code

raw_source_code = read_source_code("miniJava.java", "r")

print(raw_source_code)

lexer.input(raw_source_code)

# Tokenize
#while True:
#    tok = lexer.token()
#    if not tok:
#        break  # No more input
#    print(tok)

#parser.parse(raw_source_code, debug=True)
parser.parse(raw_source_code, lexer=lexer)
