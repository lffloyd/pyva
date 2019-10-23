#    Nossos tokens

#    'ID',         #identifier
#    'NUMBER',     #0,1,2,3...
#    'PLUS',       #+
#    'MINUS',      #-
#    'TIMES',      #*
#    'DIVIDE',     #/
#    'LPAREN',     #(
#    'RPAREN',     #)
#    'LBRACKET',   #[
#    'RBRACKET',   #]
#    'LKEY',       #{
#    'RKEY',       #}
#    'COLON',      #,
#    'SEMICOLON',  #;
#    'DOT',        #.
#    'ATTR',       #=
#    'LTHAN',      #<
#    'GTHAN',      #>
#    'LEQTHAN',    #<=
#    'GEQTHAN',    #>=
#    'EQUALS',     #==
#    'NEQUALS',    #!=
#    'AND',        #&
#    'NOT'         #!
#
#    'BOOLEAN': 'boolean',
#    'CLASS': 'class',
#    'EXTENDS': 'extends',
#    'PUBLIC': 'public',
#    'STATIC': 'static',
#    'VOID': 'void',
#    'MAIN': 'main',
#    'STRING': 'String',
#    'RETURN': 'return',
#    'INT': 'int',
#    'IF': 'if',
#    'ELSE': 'else',
#    'WHILE': 'while',
#    'SYSTEMOUTPRINTLN': 'System.out.println',
#    'LENGTH': 'length',
#    'TRUE': 'true',
#    'FALSE': 'false',
#    'THIS': 'this',
#    'NEW': 'new',
#    'NULL': 'null'

# Nossa gramática a partir da fornecida

# minúsculo são não terminais
# maiúsculo são os nossos tokes
# pode_ou_nao = representa a possibilidade de ter ou nao do EBNF

# prog -> main LKEY classe RKEY
# main -> CLASS ID LKEY PUBLIC STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET ID RPAREN LKEY cmd RKEY RKEY
# classe -> CLASS ID LBRACKET EXTENDS ID RBRACKET LKEY pode_ou_nao(var) pode_ou_nao(metodo) RKEY
# var -> tipo ID SEMICOLON
# metodo -> PUBLIC tipo ID LPAREN pode_ou_nao(params) RPAREN LKEY pode_ou_nao(var) pode_ou_nao(cmd) RETURN exp SEMICOLON RKEY
# params -> tipo ID LKEY COLON tipo ID  <--- verificar se é COLON mesmo
# tipo -> INT LBRACKET RBRACKET | BOOLEAN | INT | ID
# cmd -> LKEY pode_ou_nao(cmd) | IF LPAREN exp RPAREN cmd | IF LPAREN exp RPAREN cmd ELSE cmd | WHILE LPAREN exp RPAREN cmd | SYSTEMOUTPRINTLN LPAREN exp RPAREN SEMICOLON | ID ATTR exp SEMICOLON | ID LBRACKET exp RBRACKET ATTR exp SEMICOLON 
# exp -> exp AND rexp | rexp
# rexp -> rexp LTHAN aexp | rexp EQUALS aexp | rexp NEQUALS aexp | aexp 
# aexp -> aexp PLUS mexp | aexp MINUS mexp | mexp
# mexp -> mexp PLUS sexp | sexp
# sexp -> NOT sexp | MINUS sexp | TRUE | FALSE | NUM (verificar pois nao temos esse token) | NULL | NEW INT LBRACKET exp RBRACKET | pexp LENGTH (verificar pois na gramática dele é ".length" e na nossa é só "length") | pexp LBRACKET exp RBRACKET | pexp
# pexp -> ID | THIS | NEW ID LPAREN RPREN | LPAREN exp RPAREN | pexp ID (verificar pois na gramática dele é ".id" e a nossa é "id") | pexp ID (verificar pois na gramática dele é ".id" e a nossa é "id") LPAREN pode_ou_nao(exps) RPAREN
# exps -> exp RKEY COLON exp RKEY <--- verificar se aqui é COLON mesmo

# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from src.scanner import tokens


def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]


def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]


def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]


def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]


def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


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
