import ply.yacc as yacc
from anytree import Node

# Get the token map from the lexer.  This is required.
from .scanner import tokens

from .semantic_analysis import analiseSemantica, symbolT
from .abstract_syntax_tree.ast_node import ASTNode, create_tree
from .symtable.scope import Scope
from .symtable.symbol_table import SymbolTable
from .code_generation.mips_code_mappings import *

tree = {}

def p_prog(p):
    'prog : main conj_classes'
     
    p[0] = ASTNode(type="prog", children=p[1:], cgen=prog_cgen)

    global tree
    tree = {
        'root':  Node("prog"),
        'production': p[0]
    }


def p_main(p):
    'main : CLASS ID LKEY PUBLIC STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET ID RPAREN LKEY cmd1 RKEY RKEY'

    p[0] = ASTNode(type="main", children=p[1:], cgen=main_cgen)


def p_conj_classes(p):
    '''
    conj_classes : empty
    | conj_classes classe
    '''

    p[0] = ASTNode(type="conj_classes", children=p[1:], cgen=generic_list_of_expressions_cgen)


def p_classe(p):
    'classe : CLASS ID extension LKEY conj_var conj_metodos RKEY'
    p[0] = ASTNode(type="classe", children=p[1:])


def p_extension(p):
    '''
    extension : empty
    | EXTENDS ID
    '''
    p[0] = ASTNode(type="extension", children=p[1:], cgen=empty_cgen)


def p_conj_var(p):
    '''conj_var : empty
                | conj_var var'''

    p[0] = ASTNode(type="conj_var", children=p[1:], cgen=generic_list_of_expressions_cgen)


def p_conj_metodos(p):
    '''conj_metodos : empty
                    | conj_metodos metodo'''

    p[0] = ASTNode(type="conj_metodos", children=p[1:], cgen=generic_list_of_expressions_cgen)


def p_var(p):
    'var : tipo ID SEMICOLON'

    p[0] = ASTNode(type="var", children=p[1:])


def p_metodo(p):
    'metodo : PUBLIC tipo ID LPAREN params RPAREN LKEY conj_var conj_cmd RETURN exp SEMICOLON RKEY'

    p[0] = ASTNode(type="metodo", children=p[1:])


def p_conj_cmd(p):
    '''conj_cmd : empty
    | conj_cmd cmd1'''

    p[0] = ASTNode(type="conj_cmd", children=p[1:], cgen=generic_list_of_expressions_cgen)


def p_params(p):
    '''params : empty
    | conj_params'''

    p[0] = ASTNode(type="params", children=p[1:], cgen=generic_list_of_expressions_cgen)


def p_conj_params(p):
    '''conj_params : tipo ID mais_param'''
    p[0] = ASTNode(type="conj_params", children=p[1:])


def p_mais_param(p):
    '''mais_param : empty
    | mais_param COLON tipo ID'''

    p[0] = ASTNode(type="mais_param", children=p[1:])


def p_tipo(p):
    '''tipo : INT LBRACKET RBRACKET
    | BOOLEAN
    | INT
    | ID'''
    p[0] = ASTNode(type="tipo", children=p[1:])


def p_cmd1(p):
    '''cmd1 : LKEY conj_cmd RKEY
    | IF LPAREN exp RPAREN cmd1
    | IF LPAREN exp RPAREN cmd2 ELSE cmd1
    | WHILE LPAREN exp RPAREN cmd1
    | SYSTEMOUTPRINTLN LPAREN exp RPAREN SEMICOLON'''

    p[0] = ASTNode(type="cmd1", children=p[1:], cgen=cmd1_gen)


def p_cmd1_attr(p):
    '''cmd1 : ID ATTR exp SEMICOLON'''

    p[0] = ASTNode(type="cmd1", children=p[1:], toTable={'val': p[3].val})


def p_cmd1_attr_list(p):
    '''cmd1 : ID LBRACKET exp RBRACKET ATTR exp SEMICOLON'''

    p[0] = ASTNode(type="cmd1", children=p[1:], toTable={'val': p[6].val})


def p_cmd2(p):
    '''cmd2 : LKEY conj_cmd RKEY
      | IF LPAREN exp RPAREN cmd2 ELSE cmd2
      | WHILE LPAREN exp RPAREN cmd2
      | SYSTEMOUTPRINTLN LPAREN exp RPAREN SEMICOLON'''

    p[0] = ASTNode(type="cmd2", children=p[1:], cgen=cmd2_gen)


def p_cmd2_attr(p):
    '''cmd2 : ID ATTR exp SEMICOLON'''

    p[0] = ASTNode(type="cmd2", children=p[1:], toTable={'val': p[3].val})


def p_cmd2_attr_list(p):
    '''cmd2 : ID LBRACKET exp RBRACKET ATTR exp SEMICOLON'''

    p[0] = ASTNode(type="cmd2", children=p[1:], toTable={'val': p[6].val})


def p_exp_and(p):
    '''exp : exp AND rexp'''

    if(p[1].val != None and p[3].val != None):
        value = int(p[1].val and p[3].val)

        p[0] = ASTNode(type="aexp", children=p[1:], val=value, cgen=exp_and_cgen)
    else:
        p[0] = ASTNode(type="aexp", children=p[1:], cgen=exp_and_cgen)


def p_exp_resp(p):
    '''exp : rexp'''

    p[0] = ASTNode(type="exp", children=p[1:], val=p[1].val, cgen=generic_recursive_cgen)


def p_rexp_lthan(p):
    '''rexp : rexp LTHAN aexp'''

    if(p[1].val != None and p[3].val != None):
        value = int(p[1].val < p[3].val)

        p[0] = ASTNode(type="aexp", children=p[1:], val=value, cgen=rexp_lthan_cgen)
    else:
        p[0] = ASTNode(type="aexp", children=p[1:], cgen=rexp_lthan_cgen)


def p_rexp_equals(p):
    '''rexp : rexp EQUALS aexp'''

    if(p[1].val != None and p[3].val != None):
        value = int(p[1].val == p[3].val)
        
        p[0] = ASTNode(type="aexp", children=p[1:], val=value, cgen=rexp_equals_cgen)
    else:
        p[0] = ASTNode(type="aexp", children=p[1:], cgen=rexp_equals_cgen)


def p_rexp_nequals(p):
    '''rexp : rexp NEQUALS aexp'''

    if(p[1].val != None and p[3].val != None):
        value = int(p[1].val != p[3].val)
        # print(value)
        p[0] = ASTNode(type="aexp", children=p[1:], val=value, cgen=rexp_nequals_cgen)
    else:
        p[0] = ASTNode(type="aexp", children=p[1:], cgen=rexp_nequals_cgen)


def p_rexp_aexp(p):
    '''rexp : aexp'''

    p[0] = ASTNode(type="rexp", children=p[1:], val=p[1].val, cgen=generic_recursive_cgen)


def p_aexp_minus(p):
    '''aexp : aexp MINUS mexp'''

    if(p[1].val != None and p[3].val != None):
        value = p[1].val - p[3].val
        
        p[0] = ASTNode(type="aexp", children=p[1:], val=value, cgen=aexp_minus_cgen)
    else:
        p[0] = ASTNode(type="aexp", children=p[1:], cgen=aexp_minus_cgen)


def p_aexp_plus(p):
    '''aexp : aexp PLUS mexp'''

    if(p[1].val != None and p[3].val != None):
        value = p[1].val + p[3].val

        p[0] = ASTNode(type="aexp", children=p[1:], val=value, cgen=aexp_plus_cgen)
    else:
        p[0] = ASTNode(type="aexp", children=p[1:], cgen=aexp_plus_cgen)


def p_aexp_mexp(p):
    '''aexp : mexp'''

    p[0] = ASTNode(type="aexp", children=p[1:], val=p[1].val, cgen=generic_recursive_cgen)


def p_mexp_sexp(p):
    '''mexp : sexp'''

    # print(p[1].val)
    p[0] = ASTNode(type="mexp", children=p[1:], val=p[1].val, cgen=generic_recursive_cgen)


def p_mexp_times(p):
    '''mexp : mexp TIMES sexp'''

    value = None
    if(p[1].val == 0 or p[3].val == 0): 
        value = 0

    elif(p[1].val != None and p[3].val != None):
        value = p[1].val * p[3].val


    p[0] = ASTNode(type="mexp", children=p[1:], val=value, cgen=mexp_times_cgen)


def p_sexp(p):
    '''sexp : NEW INT LBRACKET exp RBRACKET
       | pexp DOT LENGTH
       | pexp LBRACKET exp RBRACKET'''

    p[0] = ASTNode(type="sexp", children=p[1:], cgen=sexp_cgen)


def p_sexp_not(p):
    '''sexp : NOT sexp'''

    value = None
    if (p[2].val != None):
        value = int(not p[2].val)
    p[0] = ASTNode(type="sexp", children=p[1:], val=value, cgen=sexp_not_cgent)


def p_sexp_minus(p):
    '''sexp : MINUS sexp'''

    value = None
    if (p[2].val != None):
        value = -p[2].val
    p[0] = ASTNode(type="sexp", children=p[1:], cgen=sexp_minus_cgen)


def p_sexp_pexp(p):
    '''sexp : pexp'''

    p[0] = ASTNode(type="sexp", children=p[1:], val=p[1].val, cgen=generic_recursive_cgen)


def p_sexp_terminal(p):
    '''sexp : TRUE
       | FALSE
       | NULL
       | NUMBER'''

    p[0] = ASTNode(type="sexp", children=p[1:], val=p[1], cgen=sexp_terminal_cgen)


def p_pexp_id(p):
    '''pexp : ID'''

    p[0] = ASTNode(type="pexp", children=p[1:], toTable={'val': None}, cgen=empty_cgen)


def p_pexp(p):
    '''pexp : THIS
       | LPAREN exp RPAREN
       | NEW ID LPAREN RPAREN
       | pexp DOT ID
       | pexp DOT ID LPAREN option_exps RPAREN'''

    p[0] = ASTNode(type="pexp", children=p[1:])


def p_option_exps(p):
    '''option_exps : empty
       | exp '''

    p[0] = ASTNode(type="option_exps", children=p[1:], val=p[1].val, cgen=generic_list_of_expressions_cgen)


def p_exps(p):
    '''exps : exp conj_exps '''

    p[0] = ASTNode(type="exps", children=p[1:], cgen=generic_list_of_expressions_cgen)


def p_conj_exps(p):
    '''conj_exps : empty
                 | conj_exps COLON exp'''

    p[0] = ASTNode(type="conj_exps", children=p[1:], cgen=conj_exps_cgen)


def p_empty(p):
    'empty :'
    p[0] = ASTNode(type="empty", children=[], cgen=empty_cgen)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(
            p.lineno, p.type, p.value))
    else:
        print('At end of input')


# Build the parser
parser = yacc.yacc()
