import ply.lex as lex

# List of token names.   This is always required
tokens = [
    'ID',         #identifier
    'NUMBER',     #0,1,2,3...
    'PLUS',       #+
    'MINUS',      #-
    'TIMES',      #*
    'LPAREN',     #(
    'RPAREN',     #)
    'LBRACKET',   #[
    'RBRACKET',   #]
    'LKEY',       #{
    'RKEY',       #}
    'COLON',      #,
    'SEMICOLON',  #;
    'DOT',        #.
    'ATTR',       #=
    'LTHAN',      #<
    'GTHAN',      #>
    'LEQTHAN',    #<=
    'GEQTHAN',    #>=
    'EQUALS',     #==
    'NEQUALS',    #!=
    'AND',        #&&
    'NOT',        #!
    'SYSTEMOUTPRINTLN' #System.out.println
]

# Defines the keywords
reserved_words = {
    'BOOLEAN': 'boolean',
    'CLASS': 'class',
    'EXTENDS': 'extends',
    'PUBLIC': 'public',
    'STATIC': 'static',
    'VOID': 'void',
    'MAIN': 'main',
    'STRING': 'String',
    'RETURN': 'return',
    'INT': 'int',
    'IF': 'if',
    'ELSE': 'else',
    'WHILE': 'while',
    'LENGTH': 'length',
    'TRUE': 'true',
    'FALSE': 'false',
    'THIS': 'this',
    'NEW': 'new',
    'NULL': 'null'
}

tokens += reserved_words

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LKEY = r'{'
t_RKEY = r'}'
t_COLON = r','
t_SEMICOLON = r';'
t_DOT = r'\.'
t_ATTR = r'='
t_LTHAN = r'<'
t_GTHAN = r'>'
t_LEQTHAN = r'<='
t_GEQTHAN = r'>='
t_EQUALS = r'=='
t_NEQUALS = r'!='
t_AND = r'&&'
t_NOT = r'!'


# Regular expression rules with value definitions
def t_SYSTEMOUTPRINTLN(t):
    r'System.out.println'
    t.value = str(t.value)
    return t


def t_ID(t):
    r'([a-zA-Z][0-9|a-zA-Z|_]*)'
    key = t.value.upper()
    # Adjusts the types of keyword tokens that match this regex
    if key in reserved_words:
        t.type = key
    t.value = str(t.value)
    return t


def t_NUMBER(t):
    r'(0|[1-9][0-9]*)'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
