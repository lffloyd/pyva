# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from src.scanner import tokens


class Node:
    def __init__(self,type,children=None,leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf

def p_prog(p):
    'prog : main conj_classes'
    non_terminals = [p[1], p[2]]

    p[0] = Node(type = "prog", children = non_terminals)

def p_main(p):
    'main : CLASS ID LKEY PUBLIC STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET ID RPAREN LKEY cmd1 RKEY RKEY'
    non_terminals = [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14], p[16]]
    tokens = [p[15]]

    p[0] = Node(type = "main", children = non_terminals, leaf = tokens)

def p_conj_classes(p):
    ''' 
    conj_classes : EPISILON
    | conj_classes classe
    '''

    if(len(p) > 2):
        non_terminals = [p[1], p[2]]
        p[0] = Node(type = "conj_classes", children = non_terminals)
    else:
        #caso seja a transição episilon
        pass

def p_classe(p):
    'classe : CLASS ID extension LKEY conj_var conj_metodos RKEY'
    non_terminals = [p[3], p[5], p[6]]
    tokens = [p[1], p[2], p[4], p[7]]

    p[0] = Node(type = "classe", children = non_terminals, leaf = tokens)


def p_extension(p):
    '''
    extension -> EPISILON 
    | EXTENDS ID
    '''

    if(len(p) > 2):
        tokens = [p[1], p[2]]
        Node(type = "extension", tokens = tokens)
    else:
        pass
        

        

'''

def p_prog(p):
    'prog : main LKEY classe RKEY'
    p[0] = p[3]


def p_main(p):
    'main : CLASS ID LKEY PUBLIC STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET ID RPAREN LKEY cmd RKEY RKEY'
    p[0] = p[15]

def p_classe_no_var_no_metodo(p):
    'classe : CLASS ID LBRACKET EXTENDS ID RBRACKET LKEY RKEY'
    # p[0] =
    # pass
    # Não sei qual dos dois acima a gente usaria

def p_classe_yes_var_no_metodo(p):
    'classe : CLASS ID LBRACKET EXTENDS ID RBRACKET LKEY RKEY'
    # p[0] =
    # pass
    # Não sei qual dos dois acima a gente usaria

def p_classe_no_var_no_metodo(p):
    'classe : CLASS ID LBRACKET EXTENDS ID RBRACKET LKEY RKEY'
    # p[0] =
    # pass
    # Não sei qual dos dois acima a gente usaria

def p_classe_no_var_no_metodo(p):
    'classe : CLASS ID LBRACKET EXTENDS ID RBRACKET LKEY RKEY'
    # p[0] =
    # pass
    # Não sei qual dos dois acima a gente usaria

def p_var(p):
    'var : tipo ID SEMICOLON'
    p[0] = p[1]

'''


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = """class Factorial {
    public static void main(String[] a) {
        System.out.println(new Fac().ComputeFac(10));
    }
}

class Fac {
    public int ComputeFac(int num) {
        int num_aux;
        int statica;
        if (num < 1)
            num_aux = 1;
        else
            num_aux = num * (this.ComputeFac(num - 1));
        return num_aux;
    }
}"""
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
