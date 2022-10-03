from ply.yacc import yacc
from ply.lex import lex
import sys
from utils.Constants import Operations, sem_cube, Types
from utils.FuncTable import FuncTable, Table

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
# QUADRUPLE
#######################################


class Quadruple:

    def __init__(self, op_code, left=None, right=None, target=None):
        self.op_code = op_code
        self.left = left
        self.right = right
        self.target = target

    def __str__(self):
        spaces = 20
        return f" Quad {self.op_code.value} {(spaces-len(str(self.op_code.value)))*' '}"\
            f" {self.left}{(spaces-len(str(self.left)))*' '}"\
            f" {self.right}{(spaces-len(str(self.right)))*' '}"\
            f" {self.target}"


#######################################
# PARSER
#######################################
operations_map = {
    '+': Operations.PLUS,
    '-': Operations.MINUS,
    '*': Operations.TIMES,
    '/': Operations.DIVIDE,
    '=': Operations.EQUAL,
    '<': Operations.LESSTHAN,
    '>': Operations.GREATERTHAN,
    '==': Operations.EQUALEQUAL,
    '!=': Operations.NOTEQUAL,
    '<=': Operations.LESSTHANOREQUAL,
    '>=': Operations.GREATERTHANOREQUAL,
    'goto': Operations.GOTO,
    'gotoF': Operations.GOTOF,
    'gosub': Operations.GOSUB,
    'era': Operations.ERA,
    'endFunc': Operations.ENDFUNC,
    'start': Operations.START,
    'end': Operations.END,
    'param': Operations.PARAM,
    'return': Operations.RETURN,
}

types_map = {
    'float': Types.FLOAT_TYPE,
    'bool': Types.BOOL_TYPE,
    'string': Types.STRING_TYPE,
    'void': Types.VOID,
}

# Overwrite starting rule
start = 'program'

# Global helpers
current_type = None
# Init quad list with addresses
quadruple_address_list = [Quadruple(Operations.START)]
# Init quad list with names
quadruple_name_list = [Quadruple(Operations.START)]
# Pending Operators
POper = []
# Pending Operands
PilaOperandos = []
# Coresponding types
PTypes = []
# Counter for temporary variables
temps_counter = 1
# Functions table
funcsTable = FuncTable()
# Current scope
current_scope_ref = 0
# Constants table
constants_table = {}
# Pending Jumps
PJumps = []

DIR_SIZE = 500

DIR_STRING_MAX = DIR_SIZE * 2 - 1
last_string_address = DIR_SIZE

DIR_FLOAT_MAX = DIR_SIZE * 3 - 1
last_float_address = DIR_SIZE * 2

DIR_BOOL_MAX = DIR_SIZE * 4 - 1
last_bool_address = DIR_SIZE * 3


def get_last_token(p):
    # Get last token
    token = None
    n = 1
    while not token:
        token = p[-n]
        n += 1
    return token


def create_temp_var():
    # Create a new temporary variable
    global temps_counter
    result = "$" + f"t{temps_counter}"
    temps_counter += 1
    return result


def get_var_address(var_name):
    # Get Var Address, return -1 if not found
    aux_scope_ref = current_scope_ref
    while aux_scope_ref > -1:
        if var_name in funcsTable.dict[aux_scope_ref].vars:
            var_addr = funcsTable.dict[aux_scope_ref].vars[var_name]['addr']
            return var_addr
        aux_scope_ref = funcsTable.dict[aux_scope_ref].parent_ref
    return -1


def is_constant(token):
    # Check if token is a constant
    token = str(token)
    return token[0] == '"' or token[0].isdigit() or token == "True" or token == "False"


def insert_constant(constant, constant_type):
    # insert constant in constants table
    if constant in constants_table:
        return
    constants_table[constant] = {
        'addr': get_addr(constant, constant_type),
        'type': constant_type,
    }


def check_out_of_mem(last_empty_address, max_size):
    # Check last_empty_address is not greater or equal to max_size of give type
    if(last_empty_address + 1 >= max_size):
        raise Exception("Memory ran out")


def get_addr(value, value_type):
    # Get address if it exists, or create a new one based on type of value
    if is_constant(value):
        # if token is a constant return the address from constant table if its already added
        if value in constants_table:
            return constants_table[value]['addr']
    else:
        # Check if variable already exists
        addr = get_var_address(value)
        if addr != -1:
            return addr

    # Create address fot variable or constant
    if(value_type == Types.STRING_TYPE):
        global last_string_address
        check_out_of_mem(last_string_address, DIR_STRING_MAX)
        address = last_string_address
        last_string_address += 1
    elif(value_type == Types.FLOAT_TYPE):
        global last_float_address
        check_out_of_mem(last_float_address, DIR_FLOAT_MAX)
        address = last_float_address
        last_float_address += 1
    elif(value_type == Types.BOOL_TYPE):
        global last_bool_address
        check_out_of_mem(last_bool_address, DIR_BOOL_MAX)
        address = last_bool_address
        last_bool_address += 1
    elif(value_type == Types.VOID):
        address = -1
    else:
        raise Exception('Unknown var type')

    return address


def math_operation_quadruple(operators):
    # process math operations and generate quadruple
    if len(POper) == 0:
        pass
    elif POper[-1] in operators:
        right_operand = PilaOperandos.pop()
        left_operand = PilaOperandos.pop()
        right_type = PTypes.pop()
        left_type = PTypes.pop()
        operator = POper.pop()
        result_type = sem_cube[left_type][right_type][operator]
        if result_type:
            result = create_temp_var()
            temp_quad = Quadruple(operator, left_operand,
                                  right_operand, result)
            # Add to debug quad
            quadruple_name_list.append(temp_quad)
            # Add to addr quad
            result_addr = get_addr(result, result_type)
            addr_quad = Quadruple(operator, get_addr(left_operand, left_type), get_addr(
                right_operand, right_type), result_addr)

            quadruple_address_list.append(addr_quad)

            PilaOperandos.append(result)
            PTypes.append(result_type)
            # Append temp variable to scope
            funcsTable.dict[current_scope_ref].add_variable(
                result, result_type, result_addr)
        else:
            raise Exception('Semantic error: incompatible types %s and %s in operation %s' % (
                left_type, right_type, operator))
    pass


def add_to_operand_type_stacks(token, type):
    # add operand and type to their stacks
    PilaOperandos.append(token)
    PTypes.append(type)
    pass


def p_new_scope(p):
    # New scope when you meet {}
    'new_scope : '
    global current_scope_ref
    new_scope = Table(funcsTable.dict[current_scope_ref].ref)
    funcsTable.add_scope(new_scope)
    current_scope_ref = new_scope.ref
    pass


def p_close_current_scope(p):
    # Set current scope to parent scope
    'close_current_scope : '
    global current_scope_ref
    current_scope_ref = funcsTable.dict[current_scope_ref].parent_ref
    pass


def p_add_operator_to_stack(p):
    # add operator symbol to stack
    'add_operator_to_stack : '
    POper.append(operations_map[get_last_token(p)])
    pass


def p_set_current_type(p):
    # change global current_type when you encounter float, string, bool
    'set_current_type : '
    global current_type
    current_type = types_map[get_last_token(p)]
    pass


def p_init_variable(p):
    # create variable and check if it already exists or add to current scope
    'init_variable : '
    var_name = get_last_token(p)
    # Check if variable already exists
    exists = get_var_address(var_name)
    if exists != -1:
        raise Exception(
            'Semantic error: variable %s already exists' % var_name)
    # if variable was not found in any scope generate an address for given type
    var_addr = get_addr(var_name, current_type)
    # add variable to current scope variables
    funcsTable.dict[current_scope_ref].add_variable(
        var_name, current_type, var_addr)
    pass


def p_check_variable_exists(p):
    # check variable exists and change current_type if it does
    'check_variable_exists : '
    var_name = get_last_token(p)
    exists = get_var_address(var_name)
    if exists == -1:
        raise Exception(
            'Semantic error: variable %s does not exist' % var_name)
    aux_scope_ref = current_scope_ref
    while aux_scope_ref > -1:
        if var_name in funcsTable.dict[aux_scope_ref].vars:
            global current_type
            # change current type if it exists
            current_type = funcsTable.dict[aux_scope_ref].vars[var_name]['type']
        aux_scope_ref = funcsTable.dict[aux_scope_ref].parent_ref
    pass


def p_add_id_type_to_stack(p):
    # add ID, and type to PilaOperandos and PTypes
    'add_id_type_to_stack : '
    add_to_operand_type_stacks(get_last_token(p), current_type)
    pass


def p_add_float_type_to_stack(p):
    'add_float_type_to_stack : '
    token = get_last_token(p)
    insert_constant(token, Types.FLOAT_TYPE)
    add_to_operand_type_stacks(token, Types.FLOAT_TYPE)
    pass


def p_add_string_type_stack(p):
    'add_string_type_stack : '
    token = get_last_token(p)
    insert_constant(token, Types.STRING_TYPE)
    add_to_operand_type_stacks(token, Types.STRING_TYPE)
    pass


def p_add_boolean_type_to_stack(p):
    'add_boolean_type_to_stack : '
    token = get_last_token(p)
    insert_constant(token, Types.BOOL_TYPE)
    add_to_operand_type_stacks(token, Types.BOOL_TYPE)
    pass


def p_process_relational_operator(p):
    # process 1 rel operator and 2 operands, create quadruple
    'process_relational_operator : '
    math_operation_quadruple([
        Operations.LESSTHAN,
        Operations.GREATERTHAN,
        Operations.EQUALEQUAL,
        Operations.NOTEQUAL,
        Operations.LESSTHANOREQUAL,
        Operations.GREATERTHANOREQUAL,
    ])
    pass


def p_process_plus_minus_operators(p):
    'process_plus_minus_operators : '
    math_operation_quadruple([Operations.PLUS, Operations.MINUS])
    pass


def p_process_mult_div_operators(p):
    'process_mult_div_operators : '
    math_operation_quadruple([Operations.TIMES, Operations.DIVIDE])
    pass


def p_add_separator(p):
    # Fondo falso
    'add_separator : '
    POper.append(get_last_token(p))
    pass


def p_remove_separator(p):
    # Quitar fondo falso
    'remove_separator : '
    POper.pop()
    pass


def p_create_gotof_quad(p):
    'create_gotof_quad : '
    condition_type = PTypes.pop()

    if(condition_type != Types.BOOL_TYPE):
        raise Exception('Semantic error: condition must be boolean')

    # Temporal variable or constant that contains result of condition
    condition = PilaOperandos.pop()

    # Adding to debug quad list
    quadruple_name_list.append(Quadruple(Operations.GOTOF, condition))

    # Adding to addr quad list
    quadruple_address_list.append(
        Quadruple(Operations.GOTOF, get_addr(condition, condition_type)))

    PJumps.append(len(quadruple_address_list) - 1)
    pass


def p_goto_skip_else(p):
    'goto_skip_else : '
    # Debug Quad list
    quadruple_name_list.append(Quadruple(Operations.GOTO))

    # Addr quad list
    quadruple_address_list.append(Quadruple(Operations.GOTO))

    jump_false = PJumps.pop()
    PJumps.append(len(quadruple_address_list) - 1)
    # Debug Quad list
    quadruple_name_list[jump_false].target = len(quadruple_address_list)
    # Addr quad list
    quadruple_address_list[jump_false].target = len(quadruple_address_list)
    pass


def p_goto_end_position(p):
    'goto_end_position : '
    end = PJumps.pop()
    # Debuag quad list
    quadruple_name_list[end].target = len(quadruple_address_list)
    # Addr quad list
    quadruple_address_list[end].target = len(quadruple_address_list)
    pass


def p_print_value(p):
    # Create print quadruple
    'print_value : '
    value_name = PilaOperandos.pop()
    value_type = PTypes.pop()
    # Debug Quad list
    quadruple_name_list.append(Quadruple(Operations.PRINT, target=value_name))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.PRINT, target=get_addr(value_name, value_type)))
    pass


def p_end_program(p):
    'end_program : '
    quadruple_name_list.append(Quadruple(Operations.END))
    quadruple_address_list.append(Quadruple(Operations.END))
    pass


def p_program(p):
    '''program : PROGRAM ID SEMICOLON global_declaration main_declaration end_program'''
    pass


def p_global_declaration(p):
    '''global_declaration : empty
    | global_declaration global_statement'''
    pass


def p_global_statement(p):
    '''global_statement : assign_statement
    | declare_var
    | print'''
    pass


def p_main_declaration(p):
    '''main_declaration : MAIN LPARENT RPARENT LBRACKET new_scope statement_list RBRACKET close_current_scope SEMICOLON'''
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


def p_declare_var(p):
    '''declare_var : VAR var_type ID init_variable SEMICOLON'''
    pass


def p_assign_statement(p):
    '''assign_statement : VAR var_type ID init_variable add_id_type_to_stack EQUAL add_operator_to_stack mega_expression SEMICOLON
    | reference EQUAL add_operator_to_stack mega_expression SEMICOLON'''
    pass


def p_var_type(p):
    '''var_type : FLOAT_TYPE set_current_type
    | STRING_TYPE set_current_type
    | BOOL_TYPE set_current_type'''
    pass


def p_relational_operator(p):
    '''
    relational_operator : GREATERTHAN add_operator_to_stack
    | LESSTHAN add_operator_to_stack
    | EQUALEQUAL add_operator_to_stack
    | LESSTHANOREQUAL add_operator_to_stack
    | GREATERTHANOREQUAL add_operator_to_stack
    | NOTEQUAL add_operator_to_stack
    '''
    pass


def p_mega_expression(p):
    '''
    mega_expression : expression
    | expression relational_operator expression process_relational_operator
    '''
    pass


def p_expression(p):
    '''
    expression : term process_plus_minus_operators
    | term process_plus_minus_operators PLUS add_operator_to_stack expression
    | term process_plus_minus_operators MINUS add_operator_to_stack expression
    '''
    pass


def p_term(p):
    '''
    term : factor process_mult_div_operators
    | factor process_mult_div_operators TIMES add_operator_to_stack term
    | factor process_mult_div_operators DIVIDE add_operator_to_stack term
    '''
    pass


def p_factor(p):
    '''
    factor : LPARENT add_separator mega_expression RPARENT remove_separator
    | value
    '''
    pass


def p_value(p):
    '''
    value : literal
    | reference
    '''
    pass


def p_literal(p):
    '''
    literal : FLOAT add_float_type_to_stack
    | STRING add_string_type_stack
    | TRUE add_boolean_type_to_stack
    | FALSE add_boolean_type_to_stack
    '''
    pass


def p_reference(p):
    '''reference : ID check_variable_exists add_id_type_to_stack'''
    pass


def p_if_condition(p):
    '''
    if_condition : IF LPARENT mega_expression RPARENT LBRACKET create_gotof_quad new_scope statement_list RBRACKET close_current_scope else_condition goto_end_position
    '''
    pass


def p_else_condition(p):
    '''
    else_condition : ELSE goto_skip_else LBRACKET new_scope statement_list RBRACKET close_current_scope
    | empty
    '''
    pass


def p_print(p):
    '''
    print : PRINT LPARENT mega_expression print_value RPARENT SEMICOLON
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
