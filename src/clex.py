import ply.lex as lex

# List of token names.   This is always required

reserved = (
    #keywords    
    'FOR','WHILE','BREAK',
    'IF','ELSE',
    'INT','VOID',
    'RETURN',
)

reserved_dict = {}

for r in reserved:
    reserved_dict[r.lower()] = r

tokens = reserved+(

    #identifier
    'ID',
    #operators  
    'PLUS','MINUS','TIMES','DIVIDE','MOD', # +, -, *, /, % 
    'OR','AND','NOT','LOR','LAND', 'LNOT',# |, &, ~, ||, &&, !
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE', # <, <=, >, >=, ==, !=
    'PP','MM', #++, --

    #assignment 
    'EQUALS', # =

    #literal 
    'STRING', # "~~~"
    'NUMBER',
    
    #delimiters
    'LPAREN','RPAREN','LBRACE','RBRACE','LBRACKET', 'RBRACKET', # (, ), {, }, [, ]
    'COMMA','SEMI', # , ;

    # #include 
    'INCLUDE',

    # header
    'HEADER',
)

# Regular expression rules for simple tokens

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_OR = r'\|'
t_AND = r'&'
t_NOT = r'~'
t_LOR = r'\|\|'
t_LAND = r'&&'
t_LNOT = r'!'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_PP = r'\+\+'
t_MM = r'--'
t_EQUALS = r'='
t_STRING = r'"([^"])*"'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_SEMI = r';'
t_INCLUDE = r'\#include'
t_HEADER = r'<([A-Za-z])+\.h>'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[a-zA-Z_$][0-9a-zA-Z_$]*'
    t.type = reserved_dict.get(t.value, "ID")
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


# Test it out
# Give the lexer some input

fname = input('>')

f = open(fname,'r')
data = f.read()
f.close()

lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
