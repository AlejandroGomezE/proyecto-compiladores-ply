from ply.yacc import yacc
from ply.lex import lex
import sys

#######################################
# SCANNER
#######################################

symbols = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUAL', 'LPARENT', 'RPARENT', 'SEMICOLON', 'LBRACKET',
           'RBRACKET', 'LESSTHAN', 'GREATERTHAN', 'EQUALEQUAL', 'NOTEQUAL', 'LESSTHANOREQUAL', 'GREATERTHANOREQUAL']

reserved = {
    'var': 'VAR',
    'program': 'PROGRAM',
    'float': 'FLOAT_TYPE',
    'string': 'STRING_TYPE',
    'bool': 'BOOL_TYPE',
    'True': 'TRUE',
    'False': 'FALSE',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'main': 'MAIN',
}

extras = ['ID', 'FLOAT', 'STRING']

tokens = symbols + extras + list(reserved.values())

# Ignored characters
t_ignore = ' \t'

# symbols Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_EQUAL = r'='
t_EQUALEQUAL = r'=='
t_NOTEQUAL = r'!='
t_LESSTHANOREQUAL = r'<='
t_GREATERTHANOREQUAL = r'>='


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check for reserved value
    t.type = reserved.get(t.value, 'ID')
    return t


t_FLOAT = r'((0|[1-9][0-9]*)\.[0-9][0-9]*)'
t_STRING = r'("(\\"|[^"])*")'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_COMMENT(t):
    r'\//.*'
    pass


def t_error(t):
    print("Input error: '%s'" % t.value[0])
    t.lexer.skip(1)


#######################################
# PARSER
#######################################

def p_program(p):
    '''program : PROGRAM ID SEMICOLON global_declaration main_declaration'''
    pass


def p_global_declaration_1(p):
    '''global_declaration : empty'''
    pass


def p_global_declaration_2(p):
    '''global_declaration : global_declaration global_statement'''
    pass


def p_global_statement(p):
    '''global_statement : assign_statement
    | declare_var
    | print'''
    pass


def p_var_type(p):
    '''var_type : FLOAT_TYPE
    | STRING_TYPE
    | BOOL_TYPE'''
    pass


def p_rel_operator(p):
    '''
    rel_operator : GREATERTHAN
    | LESSTHAN
    | EQUALEQUAL
    | LESSTHANOREQUAL
    | GREATERTHANOREQUAL
    | NOTEQUAL
    '''
    pass


def p_assign_statement(p):
    '''assign_statement : VAR var_type ID EQUAL expression SEMICOLON
    | ID EQUAL expression SEMICOLON'''
    pass


def p_expression(p):
    '''
    expression : exp
    | exp rel_operator exp
    '''
    pass


def p_exp(p):
    '''
    exp : term
    | term PLUS exp
    | term MINUS exp
    '''
    pass


def p_term(p):
    '''
    term : factor
    | factor TIMES term
    | factor DIVIDE term
    '''
    pass


def p_factor(p):
    '''
    factor : LPARENT expression RPARENT
    | PLUS value
    | MINUS value
    | value
    '''
    pass


def p_value(p):
    '''
    value : literal
    | reference
    '''
    pass


def p_reference(p):
    '''reference : ID'''
    pass


def p_literal(p):
    '''
    literal : FLOAT
    | STRING
    | TRUE
    | FALSE
    '''
    pass


def p_declare_var(p):
    '''declare_var : VAR var_type ID SEMICOLON'''
    pass


def p_main_declaration(p):
    '''main_declaration : MAIN LPARENT RPARENT LBRACKET statement_list RBRACKET SEMICOLON'''
    pass


def p_statement_list(p):
    '''statement_list : statement_list statement
    | empty'''
    pass


def p_statement(p):
    '''statement : declare_var
    | assign_statement
    | if_condition
    | print'''
    pass


def p_if_condition(p):
    '''
    if_condition : IF LPARENT expression RPARENT LBRACKET statement_list RBRACKET else_condition
    '''
    pass


def p_else_condition(p):
    '''
    else_condition : ELSE LBRACKET statement_list RBRACKET
    | empty
    '''
    pass


def p_print(p):
    '''
    print : PRINT LPARENT expression RPARENT SEMICOLON
    '''
    pass


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    print('Syntax error in line:', p.lineno)
    """ raise Exception("Syntax Error") """


def executeCompiler(filename):
    # Read the input file
    lines = []
    with open('./tests/' + filename) as f:
        lines = f.readlines()
    lex(optimize=1)
    # Build the parser
    parser = yacc(optimize=1, debug=False, write_tables=False)
    # Make a single string of the lines
    result = parser.parse(''.join(lines), debug=False)

    # Print the result
    print(result)


if __name__ == "__main__":
    executeCompiler(sys.argv[1])
