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
import ply.lex as lex

lexer = lex.lex()

# Give the lexer some input directory
precedence = (
        ('left','LOR'),
        ('left','LAND'),
        ('left','OR'),
        ('left','AND'),
        ('left','EQ','NE'),
        ('left','GT','GE','LT','LE'),
        ('left','PLUS','MINUS'),
        ('left','TIMES','DIVIDE','MOD'),
)

functions ={}
variables ={}

def p_translation_unit(p):
    'translation_unit : external_declaration'
    p[0]=p[1]

def p_translation_unit_append(p):
    'translation_unit : translation_unit external_declaration'
    p[1].extend(p[2])
    p[0]=p[1]

# type of exteral declarations : header, function, external declaratian(variables), just semi colon

def p_exteranal_declaration_header(p):
    'external_declaration : include_header'
    p[0] = [p[1]]

def p_include_header(p):
    'include_header : INCLUDE HEADER'
    p[0]=[p[2]]

def p_external_declaration_function(p): 
    'external_declaration : function_definition'
    p[0] = [p[1]]

def p_funciton_definition(p):
    'function_definition : id_delaration LPAREN arguments RPAREN compound_statement'
    p[0] = [p[1]]

def p_arguments(p):
    'arguments : '

def p_parameter_braces(p):
    'parameter_brace : LBRACE expression RBRACE'
    p[0] = p[2]

def p_exteranal_declaration_declaration(p):
    'external_declaration : declaration'
    p[0]=p[1]

def p_declaration(p):   
    'declaration : init_declaration SEMI'
    p[0]=p[1]

def p_init_declaration(p):
    '''init_declaration : id_declaration
                        | id_declaration array_reference
                        | id_declaration EQUALS expression'''
    p[0] = (p[1], p[3] if len(p) >3 else None)

def p_array_reference(p):
    'array_reference : LBRACKET NUMBER RBRACKET'
    p[0] = p[2]

def p_id_declaration(p):
    '''id_declaration : VOID ID
                      | INT ID'''
    p[0] = p[2]

def p_external_declaration_semi(p):
    'external_declaration : SEMI'
    p[0]=[]


def p_statement(p):
    '''statement : compound_statement
                 | iteration_statement
                 | expression_statement
                 | jump_statement
                 | slection_statement
                 '''

def p_compound_statement(p):
    'compound_statement : LBRACE block_item_list RBRACE'
    p[0]=p[2]

def p_block_item_list(p):
    '''block_item_list : block_item
                       | block_item_list block_item
    '''
    p[0] = p[1] if (len(p)==2) else p[1] + p[2]

def p_block_item(p):
    '''block_item : declaration
                  | statement
    '''
    p[0] = p[1]

def p_expression(p):
    '''expression : conditional_expression
                  | unary_expression EQUALS expression'''
    if len(p) ==2:
        p[0]=p[1]
    else:
        p[0] = p[1] = p[3]

def p_unary_expression_ppmm(p):
    'unary_expression : PP unary_expression'

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_factor(p):
    'term : factor'
    p[0]  = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Syntax error in input at %s" %p.value)

import ply.yacc as yacc

parser = yacc.yacc()

while True:
    try:
        fname = input('>')
        f = open(fname,'r')
        data = f.read()
        f.close()
    except EOFError:
        break
    if not data : continue
    result = parser.parse(data)
    print(result)
