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
data = '''
#include <stdio.h>
#include <stdlib.h>

int queue[5];
int top = 0;

void queue_push() {
    int n;
    int i;
    if (top < 5) {
        top++;
        for (i = top - 1; i > 0; i--) {
            queue[i] = queue[i - 1];
        }
        printf("\ninput : ");
        scanf("%d", &n);
        queue[0] = n;
    } else {
        printf("Queue overflow!\n");
    }
}

void queue_pop() {
    if (top == 0) {
        printf("Empty\n\n");
    } else {
        top--;
        printf("pop : %d\n\n", queue[top]);
    }
}

void queue_print() {
    int i;
    for (i = 0; i < top; i++) {
        printf("%d ", queue[i]);
    }
}

int main(void) {
    int input;
    while (1) {
        printf("\n\n1.Push (max 5) \n2.pop\n");
        scanf("%d", &input);
        if (input == 1) {
            queue_push();
            break;
        }
        if (input == 2) {
            queue_pop();
            break;


'''

# Give the lexer some input



lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
