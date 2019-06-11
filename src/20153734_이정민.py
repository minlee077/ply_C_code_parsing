#List of token names.   This is always required

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
    'PLUS','MINUS','TIMES','MOD', # +, -, *, /, % 
    'AND','LOR','LAND', 'LNOT',# |, &, ~, ||, &&, !
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

    #*header
    'HEADER',

)

# Regular expression rules for simple tokens

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_MOD = r'%'
t_AND = r'&'
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
t_HEADER = r'<([A-Za-z])+(\.h)*>'

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
        ('left','LNOT'),
        ('left','AND'),
        ('left','EQ','NE'),
        ('left','GT','GE','LT','LE'),
        ('left','PLUS','MINUS'),
        ('left','TIMES','MOD'),
)

functions ={}
variables ={}

hd_cnt = 0
fdef_cnt = 0
fcall_cnt=0
cond_cnt=0
loop_cnt=0
decvar_cnt=0

def p_translation_unit(p):
    'translation_unit : external_declaration'

def p_translation_unit_append(p):
    'translation_unit : translation_unit external_declaration'

# type of exteral declarations : header, function, external declaratian(variables), just semi colon

def p_exteranal_declaration_header(p):
    'external_declaration : include_header'

def p_empty(p):
    'empty : '

def p_include_header(p):
    'include_header : INCLUDE HEADER'
    global hd_cnt
    hd_cnt+=1

def p_external_declaration_function(p): 
    'external_declaration : function_definition'

def p_function_definition(p):
    'function_definition : id_declaration arguments compound_statement'
    global fdef_cnt
    fdef_cnt +=1

def p_arguments(p):
    'arguments : LPAREN args RPAREN'

def p_arg_list(p):
    '''args : empty
            | VOID
            | INT ID
            | INT ID COMMA INT ID
            '''

def p_external_declaration_declaration(p):
    'external_declaration : declaration'

def p_declaration(p):   
    '''declaration : init_declaration SEMI
                   '''

def p_init_declaration(p):
    '''init_declaration : id_declaration
                        | id_declaration LBRACKET NUMBER RBRACKET
                        | id_declaration EQUALS expression'''
    global decvar_cnt
    decvar_cnt +=1

def p_id_declaration(p):
    '''id_declaration : VOID ID
                      | INT ID
                      '''

def p_external_declaration_semi(p):
    'external_declaration : SEMI'

def p_statement(p):
    '''statement : compound_statement
                 | expression_statement
                 | jump_statement
                 | loop_statement
                 | condition_statement
                 '''

def p_jump_statement(p):
    '''jump_statement : BREAK SEMI
                      | RETURN SEMI
                      | RETURN expression SEMI
    '''

def p_loop_statement(p):
    '''loop_statement : FOR LPAREN expression_statement expression_statement expression_statement RPAREN statement
                      | FOR LPAREN expression_statement expression_statement expression RPAREN statement
                      | WHILE LPAREN expression RPAREN statement
    '''
    global loop_cnt
    loop_cnt +=1


def p_condition_statement(p):
    '''condition_statement  :   IF LPAREN expression RPAREN statement ELSE statement empty
                            |   IF LPAREN expression RPAREN statement
                            |   IF LPAREN expression LOR expression RPAREN  statement ELSE statement
    '''
    global cond_cnt
    cond_cnt +=1


def p_compound_statement(p):
    '''compound_statement : LBRACE declaration_list RBRACE
                          | LBRACE declaration_list statement_list RBRACE
                          | LBRACE statement_list RBRACE
                          | LBRACE RBRACE
                          '''
def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list declaration
                        '''


def p_expression_statement(p):
    '''expression_statement : SEMI
                            | expression SEMI
                            '''
def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''

def p_expression(p):
    '''expression : conditional_expression
                  | unary_expression EQUALS expression
                  | STRING 
                  '''

def p_cdd(p):
    'unary_expression : LNOT term'


def p_function_call(p):
    '''function_call : ID LPAREN expression_list RPAREN 
                     | ID LPAREN RPAREN'''
    global fcall_cnt
    fcall_cnt+=1

def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''

def p_unary_expressions(p):
    '''unary_expression : function_call
                        '''
def p_ppmm(p):
    '''expression : PP unary_expression
                  | MM unary_expression
                  | unary_expression PP
                  | unary_expression MM
                  '''


#def p_expression_plus(p):

def p_expression_and(p):
    '''unary_expression : AND term
                        '''

def p_expression_id(p):
    '''term : ID
            | ID LBRACKET NUMBER RBRACKET
            | ID LBRACKET ID RBRACKET'''



def p_term_factor(p):
    'term : factor'

def p_factor_num(p):
    'factor : NUMBER'

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'



def p_conditional_expr(p):
    '''unary_expression : term
                        | unary_expression LT term
                        | unary_expression LE term
                        | unary_expression GE term
                        | unary_expression GT term
                        | unary_expression EQ term
                        | unary_expression NE term 
                        | unary_expression AND term 
                        | unary_expression LAND unary_expression
                        | unary_expression PLUS term
                        | unary_expression TIMES term
                        | unary_expression MOD term
                        | unary_expression MINUS term
                        '''
def p_conditional_e(p):
    'conditional_expression : unary_expression'

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
    parser.parse(data)
    print("#include : %d"%hd_cnt)
    print()
    print()
    print("Declared Functions: %d"%fdef_cnt)
    print("Declared Variable: %d"%decvar_cnt)
    print()
    print()
    print("Conditional Statements: %d"%cond_cnt)
    print("Loop: %d"%loop_cnt)
    print()
    print()
    print("Called Functions: %d"%fcall_cnt)
    
    hd_cnt = 0
    fdef_cnt = 0
    fcall_cnt=0
    cond_cnt=0
    loop_cnt=0
    decvar_cnt=0

