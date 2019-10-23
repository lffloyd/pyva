#     NOSSOS TOKENS

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

#     RESERVED WORDS

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

# GRAMÁTICA ATUALIZADA EBNF ---> BNF

#        PROG -> MAIN CONJ_CLASSES
#
#        MAIN -> class id '{' public static void main '(' String '[' ']' id ')'
#        '{' CMD '}' '}'
#
#        CONJ_CLASSES -> episilon
#        | CONJ_CLASSES CLASSE
#
#        CLASSE -> class id EXTENSION '{' CONJ_VAR CONJ_METODOS '}'
#
#        EXTENSION -> episilon 
#        | extends id
#
#        CONJ_VAR -> episilon | CONJ_VAR VAR
#
#        CONJ_METODOS -> episilon | CONJ_METODOS METODO
#
#        VAR -> TIPO id ;
#
#        METODO -> public TIPO id '(' PARAMS ')' '{' CONJ_VAR CONJ_CMD return EXP ; '}'
#
#        CONJ_CMD -> episilon 
#        | CONJ_CMD CMD
#
#        PARAMS -> episilon 
#        | CONJ_PARAMS
#
#        CONJ_PARAMS -> TIPO id MAIS_PARAM
#
#        MAIS_PARAM -> episilon
#        | MAIS_PARAM , TIPO id
#
#        TIPO -> int '[' ']'
#        | boolean
#        | int
#        | id
#
#        CMD -> '{' CONJ_CMD '}'
#        | if '(' EXP ')' CMD
#        | if '(' EXP ')' CMD else CMD
#        | while '(' EXP ')' CMD
#        | System.out.println '(' EXP ')' ;
#        | id = EXP ;
#        | id '[' EXP ']' = EXP ;
#
#        EXP -> EXP && REXP
#        | REXP
#
#        REXP -> REXP < AEXP
#        | REXP == AEXP
#        | REXP != AEXP
#        | AEXP
#
#        AEXP -> AEXP + MEXP
#        | AEXP - MEXP
#        | MEXP
#
#        MEXP -> MEXP * SEXP
#        | SEXP
#
#        SEXP -> ! SEXP
#        | - SEXP
#        | true
#        | false
#        | num
#        | null
#        | new int '[' EXP ']'
#        | PEXP . length
#        | PEXP '[' EXP ']'
#        | PEXP
#
#        PEXP -> id
#        | this
#        | new id '(' ')'
#        | '(' EXP ')'
#        | PEXP . id
#        | PEXP . id '(' OPTION_EXPS ')'
#
#        OPTION_EXPS -> episilon 
#        | EXP 
#
#        EXPS -> EXP CONJ_EXPS
#
#        CONJ_EXPS -> episilon | CONJ_EXPS , EXP

# NOSSA GRAMÁTICA A PARTIR DA GRAMÁTICA ACIMA (AINDA NÃO ATUALIZEI DAQUI PRA BAIXO)

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
