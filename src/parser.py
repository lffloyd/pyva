import ply.yacc as yacc
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

# Get the token map from the lexer.  This is required.
from .scanner import tokens

from .symtable.scope import Scope
from .symtable.symbol_table import SymbolTable
from .code_generation.mips_generation import *

symbolT = SymbolTable()


class Info:
    def __init__(self, type, children=None, val=None, toTable=None, cgen=None):
        self.type = type
        self.val = val
        self.toTable = toTable
        self.cgen = cgen
        if children:
            self.children = children
        else:
            self.children = []
    def set(self, type = None, children = None, val = None):
        if type:
            self.type = type
        if children:
            self.children = children
        if val:
            self.val = val



def createTree(info, parent):
    if(info != None):
        if info.children != None:
            index = 0
            for item in info.children:
                if not type(item) is Info:
                    Node(str(item), parent=parent)
                else:
                    new = Node(item.type, parent=parent)
                    createTree(item, new)

def analiseSemantica(info, constante=0):
    global symbolT
    if(info != None and type(info) is Info):
        if info.children != None:
            index = 0
            for item in info.children:
                if type(item) is Info:  # TODO trocar para not
                    #if item.val != None and len(item.children):  # TODO apagar apos implementacao
                        #print(item.val)
                        #item[index].info = item.val
                        #item[index].children = []
                # else:
                    if (item.type == "class"):
                        symbolT = SymbolTable()
                        analiseSemantica(item)

                    elif (item.type == "metodo"):
                        symbolT.insert_scope(Scope())
                        analiseSemantica(item)
                        symbolT.remove()
                    else:
                        if (item.type == "mexp" ):
                            constante = 0
                        if (item.type == "aexp"):
                            if(item.val):
                                info.children[index] = item.val + constante
                                return True
                            elif len(item.children) > 1:                            
                                if(item.children[1] and item.children[2].val != None):
                                    item.children[2] = item.children[2].val
                                    if(item.children[1] == "+" ):
                                        constante = constante + item.children[2]
                                        item.children[2] = constante
                                        resp = analiseSemantica(item, constante)
                                        if resp :
                                            item.set(children = [item.children[0]])
                                        return True
                                    if(item.children[1] == "-" ):
                                        constante = constante - item.children[2]
                                        item.children[2] = constante
                                        resp = analiseSemantica(item, constante)
                                        if resp :
                                            item.set(children = [item.children[0]])
                                        return True
                                elif(item.children[1] and item.children[0].val != None):
                                    item.children[0] = item.children[0].val
                                    if(item.children[1] == "+" ):
                                        constante = constante + item.children[0]
                                        item.children[0] = constante
                                        resp = analiseSemantica(item, constante)
                                        if resp :
                                            item.set(children = [item.children[2]])
                                        return True
                                    if(item.children[1] == "-" ):
                                        constante = constante - item.children[0]
                                        item.children[0] = constante
                                        resp = analiseSemantica(item, constante)
                                        if resp :
                                            item.set(children = [item.children[2]])
                                        return True
                                    return None
                                else:
                                    return analiseSemantica(item, constante)
                        else:
                            if (item.type == "var" or item.type == "conj_params"):
                                
                                if (len(item.children[0].children) > 1):
                                    
                                    symbolT.insert_entry(
                                        item.children[1], {'type': 'int[]'})
                                else:
                                    symbolT.insert_entry(item.children[1], {
                                                        'type': item.children[0].children[0]})

                            elif (item.type == "mais_param" and len(item.children) > 1):
                                if (len(item.children[2].children) > 1):
                                    symbolT.insert_entry(
                                        item.children[3], {'type': 'int[]'})
                                else:
                                    symbolT.insert_entry(item.children[3], {
                                                        'type': item.children[2].children[0]})

                            elif ((item.type == "pexp" or item.type == "cmd2" or item.type == "cmd1") and item.toTable):
                                sco = symbolT.scopes[symbolT.current_scope_level]
                                glob = symbolT.scopes[0]
                                
                                if not (sco.is_in(item.children[0]) or glob.is_in(item.children[0])):
                                    print('Erro: Variável {0} não declarada'.format(
                                        item.children[0]))
                            
                            analiseSemantica(item)
                index += 1
                            
def p_prog(p):
    'prog : main conj_classes'
     
    p[0] = Info(type="prog", children=p[1:], cgen=prog_cgen)
    raiz_arvore = p[0]
    raiz_arvore.cgen(p)
    root = Node("prog")
    analiseSemantica(p[0])
    createTree(p[0], root)
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))
    # DotExporter(root).to_picture("root.png")


def p_main(p):
    'main : CLASS ID LKEY PUBLIC STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET ID RPAREN LKEY cmd1 RKEY RKEY'

    p[0] = Info(type="main", children=p[1:], cgen=main_cgen)


def p_conj_classes(p):
    '''
    conj_classes : empty
    | conj_classes classe
    '''

    p[0] = Info(type="conj_classes", children=p[1:], cgen=conj_classes_cgen)


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
    | SYSTEMOUTPRINTLN LPAREN exp RPAREN SEMICOLON'''

    p[0] = Info(type="cmd1", children=p[1:])


def p_cmd1_attr(p):
    '''cmd1 : ID ATTR exp SEMICOLON'''

    p[0] = Info(type="cmd1", children=p[1:], toTable={'val': p[3].val})


def p_cmd1_attr_list(p):
    '''cmd1 : ID LBRACKET exp RBRACKET ATTR exp SEMICOLON'''

    p[0] = Info(type="cmd1", children=p[1:], toTable={'val': p[6].val})


def p_cmd2(p):
    '''cmd2 : LKEY conj_cmd RKEY
      | IF LPAREN exp RPAREN cmd2 ELSE cmd2
      | WHILE LPAREN exp RPAREN cmd2
      | SYSTEMOUTPRINTLN LPAREN exp RPAREN SEMICOLON'''

    p[0] = Info(type="cmd2", children=p[1:])


def p_cmd2_attr(p):
    '''cmd2 : ID ATTR exp SEMICOLON'''

    p[0] = Info(type="cmd2", children=p[1:], toTable={'val': p[3].val})


def p_cmd2_attr_list(p):
    '''cmd2 : ID LBRACKET exp RBRACKET ATTR exp SEMICOLON'''

    p[0] = Info(type="cmd2", children=p[1:], toTable={'val': p[6].val})


def p_exp_and(p):
    '''exp : exp AND rexp'''

    if(p[1].val != None and p[3].val != None):
        value = p[1].val and p[3].val
        # print(value)
        p[0] = Info(type="aexp", children=p[1:], val=value)
    else:
        p[0] = Info(type="aexp", children=p[1:])


def p_exp_resp(p):
    '''exp : rexp'''

    p[0] = Info(type="exp", children=p[1:], val=p[1].val)


def p_rexp_lthan(p):
    '''rexp : rexp LTHAN aexp'''

    if(p[1].val != None and p[3].val != None):
        value = p[1].val < p[3].val
        # print(value)
        p[0] = Info(type="aexp", children=p[1:], val=value)
    else:
        p[0] = Info(type="aexp", children=p[1:])


def p_rexp_equals(p):
    '''rexp : rexp EQUALS aexp'''

    if(p[1].val != None and p[3].val != None):
        value = p[1].val == p[3].val
        # print(value)
        p[0] = Info(type="aexp", children=p[1:], val=value)
    else:
        p[0] = Info(type="aexp", children=p[1:])


def p_rexp_nequals(p):
    '''rexp : rexp NEQUALS aexp'''

    if(p[1].val != None and p[3].val != None):
        value = p[1].val != p[3].val
        # print(value)
        p[0] = Info(type="aexp", children=p[1:], val=value)
    else:
        p[0] = Info(type="aexp", children=p[1:])


def p_rexp_aexp(p):
    '''rexp : aexp'''

    p[0] = Info(type="rexp", children=p[1:], val=p[1].val)


def p_aexp_minus(p):
    '''aexp : aexp MINUS mexp'''

    if(p[1].val != None and p[3].val != None):
        value = p[1].val - p[3].val
        # print(value)
        p[0] = Info(type="aexp", children=p[1:], val=value)
    else:
        p[0] = Info(type="aexp", children=p[1:])


def p_aexp_plus(p):
    '''aexp : aexp PLUS mexp'''

    if(p[1].val != None and p[3].val != None):
        value = p[1].val + p[3].val
        p[0] = Info(type="aexp", children=p[1:], val=value)
    else:
        p[0] = Info(type="aexp", children=p[1:])


def p_aexp_mexp(p):
    '''aexp : mexp'''

    p[0] = Info(type="aexp", children=p[1:], val=p[1].val)


def p_mexp_sexp(p):
    '''mexp : sexp'''

    # print(p[1].val)
    p[0] = Info(type="mexp", children=p[1:], val=p[1].val)


def p_mexp_times(p):
    '''mexp : mexp TIMES sexp'''

    value = None
    if(p[1].val != None and p[3].val != None):
        value = p[1].val * p[3].val
    if(p[1].val == 0 or p[3].val == 0): 
        value = 0
        # print(val)
    p[0] = Info(type="mexp", children=p[1:], val=value)


def p_sexp(p):
    '''sexp : NEW INT LBRACKET exp RBRACKET
       | pexp DOT LENGTH
       | pexp LBRACKET exp RBRACKET'''

    p[0] = Info(type="sexp", children=p[1:])


def p_sexp_not(p):
    '''sexp : NOT sexp'''

    value = None
    if (p[2].val != None):
        value = not p[2].val
    p[0] = Info(type="sexp", children=p[1:], val=value)


def p_sexp_minus(p):
    '''sexp : MINUS sexp'''

    value = None
    if (p[2].val != None):
        value = -p[2].val
    p[0] = Info(type="sexp", children=p[1:])


def p_sexp_pexp(p):
    '''sexp : pexp'''

    p[0] = Info(type="sexp", children=p[1:], val=p[1].val)


def p_sexp_terminal(p):
    '''sexp : TRUE
       | FALSE
       | NULL
       | NUMBER'''

    p[0] = Info(type="sexp", children=p[1:], val=p[1])


def p_pexp_id(p):
    '''pexp : ID'''

    p[0] = Info(type="pexp", children=p[1:], toTable={'val': None})


def p_pexp(p):
    '''pexp : THIS
       | LPAREN exp RPAREN
       | NEW ID LPAREN RPAREN
       | pexp DOT ID
       | pexp DOT ID LPAREN option_exps RPAREN'''

    p[0] = Info(type="pexp", children=p[1:])


def p_option_exps(p):
    '''option_exps : empty
       | exp '''

    p[0] = Info(type="option_exps", children=p[1:], val=p[1].val, cgen=option_exps)


def p_exps(p):
    '''exps : exp conj_exps '''

    p[0] = Info(type="exps", children=p[1:], cgen=exps_cgen)


def p_conj_exps(p):
    '''conj_exps : empty
                 | conj_exps COLON exp'''

    p[0] = Info(type="conj_exps", children=p[1:], cgen=conj_exps_cgen)


def p_empty(p):
    'empty :'
    p[0] = Info(type="empty", children=[], cgen=empty_cgen)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(
            p.lineno, p.type, p.value))
    else:
        print('At end of input')


# Build the parser
parser = yacc.yacc()
