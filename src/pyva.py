from sys import argv
from anytree import Node, RenderTree

from .scanner import lexer
from .parser import parser
from .semantic_analysis import analiseSemantica
from .code_generation.mips_generator import MIPSGenerator
from .abstract_syntax_tree.ast_node import create_tree
from .utils.code_reader import read_source_code
from .utils.code_writer import write_assembly_code


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
        print('***************Token list:**************')

        lexer.input(raw_source_code)

        while True:
            tok = lexer.token()
            if not tok:
                break  # No more input
            print(tok)

        print('****************************************\n')
        print('**************Syntax tree:**************')

        parser.parse(raw_source_code, lexer=lexer)

        from .parser import tree

        create_tree(tree['production'], tree['root'])
        for pre, _, node in RenderTree(tree['root']):
            print("%s%s" % (pre, node.name))

        print('****************************************\n')

        print('****************************************\n')

        print('**************MIPS Code Generation:**************')

        from .parser import tree

        mips_gen = MIPSGenerator()
        code = mips_gen.generate_code(tree)

        print(code)

        write_assembly_code(argv[1], 'w', code)

        print('****************************************\n')
        print('**************Semantic analysis:**************')

        from .parser import tree
        
        try:
            analiseSemantica(tree['production'])
            tree['root'] = Node("prog")
            create_tree(tree['production'], tree['root'])
            for pre, _, node in RenderTree(tree['root']):
                print("%s%s" % (pre, node.name))
        except Exception as e:
            print(e)
        print('****************************************\n')


    except FileNotFoundError as err:
        print(err)
    except IndexError as err:
        print(err)