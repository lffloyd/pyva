import ply.yacc as yacc
#from treelib import Node, Tree
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

# Get the token map from the lexer.  This is required.
from src.scanner import tokens

#globalId = 0
#tree = Tree()

class Info:
    def __init__(self, type, children=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []

def createTree(info, parent):
    if(info != None):
        if info.children != None:
            for item in info.children:
                if not type(item) is Info:
                    Node(str(item), parent = parent)
                else:
                    new = Node(item.type, parent=parent)
                    createTree(item, new)


def p_prog(p):
    'prog : main conj_classes'
    p[0] = Info(type="prog", children=p[1:])
    root = Node("prog")
    createTree(p[0], root)
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))
    DotExporter(root).to_picture("root.png")


def p_main(p):
    'main : CLASS ID LKEY PUBLIC STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET ID RPAREN LKEY cmd1 RKEY RKEY'
    
    p[0] = Info(type="main", children=p[1:])


def p_conj_classes(p):
    '''
    conj_classes : empty
    | conj_classes classe
    '''

    p[0] = Info(type="conj_classes", children=p[1:])


def p_classe(p):
    'classe : CLASS ID extension LKEY conj_var conj_metodos RKEY'

    p[0] = Info(type="classe", children=p[1:])


def p_extension(p):
    '''
    extension : empty
    | EXTENDS ID
    '''
    p[0] = Info(type="extension", children=p[1:])


def p_conj_var(p):
    '''conj_var : empty
                | conj_var var'''

    p[0] = Info(type="conj_var", children=p[1:])


def p_conj_metodos(p):
    '''conj_metodos : empty
                    | conj_metodos metodo'''

    p[0] = Info(type="conj_metodos", children=p[1:])


def p_var(p):
    'var : tipo ID SEMICOLON'

    p[0] = Info(type="var", children=p[1:])


def p_metodo(p):
    'metodo : PUBLIC tipo ID LPAREN params RPAREN LKEY conj_var conj_cmd RETURN exp SEMICOLON RKEY'

    p[0] = Info(type="metodo", children=p[1:])


def p_conj_cmd(p):
    '''conj_cmd : empty
    | conj_cmd cmd1'''

    p[0] = Info(type="conj_cmd", children=p[1:])


def p_params(p):
    '''params : empty
    | conj_params'''

    p[0] = Info(type="params", children=p[1:])


def p_conj_params(p):
    '''conj_params : tipo ID mais_param'''

    p[0] = Info(type="conj_params", children=p[1:])


def p_mais_param(p):
    '''mais_param : empty
    | mais_param COLON tipo ID'''

    p[0] = Info(type="mais_param", children=p[1:])


def p_tipo(p):
    '''tipo : INT LBRACKET RBRACKET
    | BOOLEAN
    | INT
    | ID'''

    p[0] = Info(type="tipo", children=p[1:])


def p_cmd1(p):
    '''cmd1 : LKEY conj_cmd RKEY
    | IF LPAREN exp RPAREN cmd1
    | IF LPAREN exp RPAREN cmd2 ELSE cmd1
    | WHILE LPAREN exp RPAREN cmd1
    | SYSTEMOUTPRINTLN LPAREN exp RPAREN SEMICOLON
    | ID ATTR exp SEMICOLON
    | ID LBRACKET exp RBRACKET ATTR exp SEMICOLON'''

    p[0] = Info(type="cmd1", children=p[1:])


def p_cmd2(p):
    '''cmd2 : LKEY conj_cmd RKEY
      | IF LPAREN exp RPAREN cmd2 ELSE cmd2
      | WHILE LPAREN exp RPAREN cmd2
      | SYSTEMOUTPRINTLN LPAREN exp RPAREN SEMICOLON
      | ID ATTR exp SEMICOLON
      | ID LBRACKET exp RBRACKET ATTR exp SEMICOLON'''

    p[0] = Info(type="cmd2", children=p[1:])


def p_exp(p):
    '''exp : exp AND rexp
        | rexp'''

    p[0] = Info(type="exp", children=p[1:])


def p_rexp(p):
    '''rexp : rexp LTHAN aexp
        | rexp EQUALS aexp
        | rexp NEQUALS aexp
        | aexp'''

    p[0] = Info(type="rexp", children=p[1:])


def p_aexp(p):
    '''aexp : aexp PLUS mexp
        | aexp MINUS mexp
        | mexp'''

    p[0] = Info(type="aexp", children=p[1:])


def p_mexp(p):
    '''mexp : mexp TIMES sexp
        | sexp'''

    p[0] = Info(type="mexp", children=p[1:])


def p_sexp(p):
    '''sexp : NOT sexp
       | MINUS sexp
       | TRUE
       | FALSE
       | NUMBER
       | NULL
       | NEW INT LBRACKET exp RBRACKET
       | pexp DOT LENGTH
       | pexp LBRACKET exp RBRACKET
       | pexp'''

    p[0] = Info(type="sexp", children=p[1:])


def p_pexp(p):
    '''pexp : ID
       | THIS
       | LPAREN exp RPAREN
       | NEW ID LPAREN RPAREN
       | pexp DOT ID
       | pexp DOT ID LPAREN option_exps RPAREN'''

    p[0] = Info(type="pexp", children=p[1:])

def p_option_exps(p):
    '''option_exps : empty
       | exp '''

    p[0] = Info(type="option_exps", children=p[1:])


def p_exps(p):
    '''exps : exp conj_exps '''

    p[0] = Info(type="exps", children=p[1:])


def p_conj_exps(p):
    '''conj_exps : empty
                 | conj_exps COLON exp'''

    p[0] = Info(type="conj_exps", children=p[1:])


def p_empty(p):
    'empty :'
    p[0] = Info(type="empty", children = [])


def p_error(p):
        if p:
            print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        else:
            print('At end of input')


# Build the parser
parser = yacc.yacc()
