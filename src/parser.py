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
    extension : EPISILON 
    | EXTENDS ID
    '''

    if(len(p) > 2):
        tokens = [p[1], p[2]]
        p[0] = Node(type = "extension", leaf = tokens)
    else:
        pass

def p_conj_var(p):
    '''conj_var : EPISILON | conj_var var'''

    if(len(p) > 2):
        non_terminals = [p[1], p[2]]
        p[0] = Node(type="conj_var", children=non_terminals)
    else:
        pass

def p_conj_metodos(p):
    '''conj_metodos : EPISILON | conj_metodos metodo'''

    if(len(p) > 2):
        non_terminals = [p[1], p[2]]
        p[0] = Node(type="conj_metodos", children=non_terminals)
    else:
        pass

def p_var(p):
    'var : tipo ID SEMICOLON'

    non_terminals = [p[1]]
    tokens = [p[2], p[3]]
    p[0] = Node(type="var", children=non_terminals, leaf=tokens)

def p_metodo(p):
    'metodo : PUBLIC tipo ID LPAREN params RPAREN LKEY conj_var conj_cmd RETURN exp SEMICOLON RKEY'

    tokens = [p[1], p[3], p[4], p[6], p[7], p[10], p[12], p[13]]
    non_terminals = [p[2], p[5], p[8], p[9], p[11]]
    p[0] = Node(type="metodo", children=non_terminals, leaf=tokens)

def p_conj_cmd(p):
    '''conj_cmd : EPISILON 
    | conj_cmd cmd'''

    if(len(p) > 2):
        non_terminals = [p[1], p[2]]
        p[0] = Node(type="conj_cmd", children=non_terminals)
    else:
        pass

def p_params_episilon(p):
    'params : EPISILON'
    pass

def p_params_conj(p):
    'params : conj_params'
    non_terminals = [p[1]]
    p[0] = Node(type="params", children=non_terminals)

def p_conj_params(p):
    '''conj_params : tipo ID mais_param'''

    non_terminals = [p[1], p[3]]
    tokens = [p[2]]
    p[0] = Node(type="conj_params", children=non_terminals, leaf=tokens)

def p_mais_param(p):
    '''mais_param : EPISILON 
    | mais_param COLON tipo ID'''

    if(len(p) > 2):
        non_terminals = [p[1], p[3]]
        tokens = [p[2], p[4]]
        p[0] = Node(type="mais_param", children=non_terminals, leaf=tokens)
    else:
        pass

def p_tipo_array(p):
    'tipo: INT LBRACKET RBRACKET'

    tokens = [p[1], p[2], p[3]]
    p[0] = Node(type="tipo", leaf=tokens)

def p_tipo_boolean(p):
    'tipo: BOOLEAN'

    tokens = [p[1]]
    p[0] = Node(type="tipo", leaf=tokens)

def p_tipo_int(p):
    'tipo: INT '

    tokens = [p[1]]
    p[0] = Node(type="tipo", leaf=tokens)

def p_tipo_id(p):
    'tipo: ID'

    tokens = [p[1]]
    p[0] = Node(type="tipo", leaf=tokens)

def p_exp(p):
    '''exp : exp AND rexp
        | rexp'''

    if(len(p) > 2):
        non_terminals = [p[1], p[3]]
        tokens = [p[2]]
        p[0] = Node(type="tipo", children=non_terminals, leaf=tokens)
    else:
        non_terminals = [p[1]]
        p[0] = Node(type="tipo", children=non_terminals)



#        cmd1 -> LKEY conj_cmd RKEY
#        | IF LPAREN exp RPAREN cmd1
#        | IF LPAREN exp RPAREN cmd2 ELSE cmd1
#        | WHILE LPAREN exp RPAREN cmd1
#        | sYSTEM.OUT.PRINTLN LPAREN exp RPAREN SEMICOLON
#        | ID ATTR exp SEMICOLON
#        | ID LBRACKET exp RBRACKET ATTR exp SEMICOLON
#
#        cmd2 -> LKEY conj_cmd RKEY
#        | IF LPAREN exp RPAREN cmd2 ELSE cmd2
#        | WHILE LPAREN exp RPAREN cmd2
#        | SYSTEMOUTPRINTLN LPAREN exp RPAREN SEMICOLON
#        | ID ATTR exp SEMICOLON
#        | ID LBRACKET exp RBRACKET ATTR exp SEMICOLON
#          

#        rexp -> rexp LTHAN aexp
#        | rexp EQUALS aexp
#        | rexp NEQUALS aexp
#        | aexp
#
#        aexp -> aexp PLUS mexp
#        | aexp MINUS mexp
#        | mexp
#
#        mexp -> mexp TIMES sexp
#        | sexp
#
#        sexp -> NOT sexp
#        | MINUS sexp
#        | TRUE
#        | FALSE
#        | NUM
#        | NULL
#        | NEW INT LBRACKET exp RBRACKET
#        | pexp DOT LENGTH
#        | pexp LBRACKET exp RBRACKET
#        | pexp
#
#        pexp -> ID
#        | THIS
#        | NEW ID LPAREN RPAREN
#        | LPAREN exp RPAREN
#        | pexp DOT ID
#        | pexp DOT ID LPAREN option_exps RPAREN
#
#        option_exps -> EPISILON 
#        | exp 
#
#        exps -> exp conj_exps
#
#        conj_exps -> EPISILON | conj_exps COLON exp        

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
