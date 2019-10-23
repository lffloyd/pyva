# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from src.scanner import tokens


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
