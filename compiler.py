from ply.yacc import yacc
from ply.lex import lex
import sys
from utils.Constants import Operations, sem_cube, Types
from utils.FuncTable import FuncTable, Table

#######################################
# SCANNER
#######################################

symbols = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUAL', 'LPARENT', 'RPARENT', 'SEMICOLON', 'LBRACE',
           'RBRACE', 'LBRACKET', 'RBRACKET', 'LESSTHAN', 'GREATERTHAN', 'EQUALEQUAL', 'NOTEQUAL', 'LESSTHANOREQUAL', 'GREATERTHANOREQUAL', 'COMMA']

reserved = {
    'var': 'VAR',
    'program': 'PROGRAM',
    'float': 'FLOAT_TYPE',
    'int': 'INT_TYPE',
    'string': 'STRING_TYPE',
    'bool': 'BOOL_TYPE',
    'void': 'VOID_TYPE',
    'True': 'TRUE',
    'False': 'FALSE',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'main': 'MAIN',
    'absolute': 'ABSOLUTE',
    'sqrt': 'SQRT',
    'trunc': 'TRUNC',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'read': 'READ',
    'substr': 'SUBSTR',
    'toLower': 'TOLOWER',
    'toUpper': 'TOUPPER',
    'avg': 'AVG',
    'sort': 'SORT',
    'find': 'FIND',
    'min': 'MIN',
    'max': 'MAX',
    'sum': 'SUM',
    'len': 'LEN',
}

extras = ['ID', 'INT', 'FLOAT', 'STRING']

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
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
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


t_FLOAT = r'[-]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
t_INT = r'(0|[-]?[1-9][0-9]*)'
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
}

types_map = {
    'float': Types.FLOAT_TYPE,
    'int': Types.INT_TYPE,
    'bool': Types.BOOL_TYPE,
    'string': Types.STRING_TYPE,
    'void': Types.VOID_TYPE,
}

# Overwrite starting rule
start = 'program'

# Global helpers
current_type = None
# Init quad list with addresses
quadruple_address_list = [
    Quadruple(Operations.START)]
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
# Function declared stack
last_func_call = []
# Array stack
array_name_stack = []
# Array size stack
array_size_stack = []
# Virtual vars stack
virtual_var_list = []
# Return counter
return_counter = 0
# Argument counter for function calls
argument_counter = 0

DIR_SIZE = 500

DIR_STRING_MAX = DIR_SIZE * 2 - 1
last_string_address = DIR_SIZE

DIR_FLOAT_MAX = DIR_SIZE * 3 - 1
last_float_address = DIR_SIZE * 2

DIR_BOOL_MAX = DIR_SIZE * 4 - 1
last_bool_address = DIR_SIZE * 3

DIR_INT_MAX = DIR_SIZE * 5 - 1
last_int_address = DIR_SIZE * 4


def init_compiler():
    # Resets every global helper
    global current_type
    global quadruple_address_list
    global quadruple_name_list
    global POper
    global PilaOperandos
    global PTypes
    global temps_counter
    global funcsTable
    global current_scope_ref
    global constants_table
    global PJumps
    global last_func_call
    global array_name_stack
    global array_size_stack
    global virtual_var_list
    global argument_counter
    global last_string_address
    global last_float_address
    global last_bool_address
    global last_int_address
    global return_counter

    current_type = None
    # List of quadruples with addresses
    quadruple_address_list = [
        Quadruple(Operations.START)]
    # List of quadruples
    quadruple_name_list = [
        Quadruple(Operations.START)]

    # Scope tree for storing variables and functions
    funcsTable = FuncTable()
    current_scope_ref = 0
    constants_table = {}
    # Pending Operators
    POper = []
    # Pending Operands
    PilaOperandos = []
    # Coresponding types
    PTypes = []
    # Pending Jumps
    PJumps = []
    # Function declared stack
    last_func_call = []
    # Array stack
    array_name_stack = []
    # Array size stack
    array_size_stack = []
    # Virtual vars stack
    virtual_var_list = []
    # Return counter
    return_counter = 0
    # Argument counter for function calls
    argument_counter = 0
    # Counter for used temporary variables
    temps_counter = 1
    last_string_address = DIR_SIZE
    last_float_address = DIR_SIZE * 2
    last_bool_address = DIR_SIZE * 3
    last_int_address = DIR_SIZE * 4


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


def create_temp_virtual_var():
    # Create a new temporary variable
    global temps_counter
    result = "V" + f"t{temps_counter}"
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


def get_func_ref(aux_scope_ref, function_name):
    # Get func_name ref, look in current aux_scope_ref and all its parents
    while(aux_scope_ref > -1):
        # check if function ref exists in current aux_scope_ref
        if function_name in funcsTable.dict[aux_scope_ref].functions:
            # return function ref
            return funcsTable.dict[aux_scope_ref].functions[function_name]
        # go to parent scope
        aux_scope_ref = funcsTable.dict[aux_scope_ref].parent_ref
    # If not found, return -1
    return -1


def is_constant(token):
    # Check if token is a constant
    token = str(token)
    return token[0] == '"' or token[0].isdigit() or (token[0] == '-' and token[1].isdigit()) or token == "True" or token == "False"


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
    elif(value_type == Types.INT_TYPE):
        global last_int_address
        check_out_of_mem(last_int_address, DIR_INT_MAX)
        address = last_int_address
        last_int_address += 1
    elif(value_type == Types.BOOL_TYPE):
        global last_bool_address
        check_out_of_mem(last_bool_address, DIR_BOOL_MAX)
        address = last_bool_address
        last_bool_address += 1
    elif(value_type == Types.VOID_TYPE):
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
            # Add to debug quad
            quadruple_name_list.append(Quadruple(operator, left_operand,
                                                 right_operand, result))
            # Add to addr quad
            result_addr = get_addr(result, result_type)

            quadruple_address_list.append(Quadruple(operator, get_addr(left_operand, left_type), get_addr(
                right_operand, right_type), result_addr))

            PilaOperandos.append(result)
            PTypes.append(result_type)
            # Append temp variable to scope
            funcsTable.dict[current_scope_ref].add_variable(
                result, result_type, result_addr)
        else:
            raise Exception('Semantic error: Incompatible types "%s" and "%s" in operation "%s"' % (
                left_type.value, right_type.value, operator.value))
    pass


def assign_var():
    if len(POper) == 0:
        pass
    elif POper[-1] in [Operations.EQUAL]:
        left_operand = PilaOperandos.pop()
        left_type = PTypes.pop()
        right_operand = PilaOperandos.pop()
        right_type = PTypes.pop()
        operator = POper.pop()
        result_type = sem_cube[left_type][right_type][operator]
        if result_type:
            # Debug quad list
            quadruple_name_list.append(
                Quadruple(operator, left_operand, target=right_operand))
            # Addr quad list
            quadruple_address_list.append(Quadruple(operator, get_addr(
                left_operand, left_type), target=get_addr(right_operand, right_type)))
        else:
            raise Exception('Semantic error: Incompatible types "%s" and "%s" in assignment.' % (
                left_type.value, right_type.value))


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


def p_set_func_return_type(p):
    # Set function return type
    'set_func_return_type : '
    funcsTable.dict[current_scope_ref].return_type = types_map[get_last_token(
        p)]
    pass


def p_new_function_scope(p):
    # New function scope
    'new_function_scope : '
    global current_scope_ref
    function_name = get_last_token(p)
    # Add function to current scope functions, no content yet
    funcsTable.dict[current_scope_ref].functions[function_name] = -1
    # Create new scope for function add its name
    new_scope = Table(funcsTable.dict[current_scope_ref].ref)
    new_scope.function_name = function_name
    # Add function scope to funcsTable
    funcsTable.add_scope(new_scope)
    # Add new function scope ref to parent scope ('current_scope_ref' => where function was declared)
    funcsTable.dict[current_scope_ref].functions[function_name] = new_scope.ref
    # Add new function scope_ref and function_name to its own functionsTable to allow recursion calls
    current_scope_ref = new_scope.ref
    funcsTable.dict[current_scope_ref].functions[function_name] = current_scope_ref
    pass


def p_init_param(p):
    # Create or find address for var_name and add to current scope as var, and param
    'init_param : '
    param_name = get_last_token(p)
    exists = get_var_address(param_name)
    if exists != -1:
        raise Exception(
            'Semantic error: Name for parameter "%s" is already used.' % param_name)

    param_addr = get_addr(param_name, current_type)
    # Add param name to variable list of function scope
    funcsTable.dict[current_scope_ref].add_variable(
        param_name, current_type, param_addr)
    # Add param name to param list of function scope
    funcsTable.dict[current_scope_ref].add_parameter(param_name)
    pass


def p_function_start_quad(p):
    # Set start position for function block
    'function_start_quad : '
    funcsTable.dict[current_scope_ref].quad_start = len(
        quadruple_address_list)
    pass


def p_endfunc_quad(p):
    'endfunc_quad : '
    global return_counter
    if funcsTable.dict[current_scope_ref].function_name != None:
        if(funcsTable.dict[current_scope_ref].return_type != types_map['void'] and return_counter == 0):
            raise Exception(
                "Semantic error: Function %s must have a return statement." % funcsTable.dict[current_scope_ref].function_name)

    return_counter = 0
    # Debug quad list
    quadruple_name_list.append(Quadruple(Operations.ENDFUNC))
    # Addr quad list
    quadruple_address_list.append(Quadruple(Operations.ENDFUNC))
    pass


def p_init_func_call(p):
    # Check function exists, to ERA quad, fondo falso in case of z = 2 + 2 + function(1.0+1.0)
    'init_func_call : '
    POper.append('(')
    function_name = get_last_token(p)
    global last_func_call
    last_func_call.append(function_name)
    # Get func_name ref check current scope and all parent scopes
    function_ref = get_func_ref(current_scope_ref, function_name)
    if function_ref == -1:
        raise Exception(
            'Semantic error: Function "%s" is not declared.' % function_name)

    # Debug quad list
    quadruple_name_list.append(Quadruple(Operations.ERA, target=function_name))
    # Addr quad list
    quadruple_address_list.append(
        Quadruple(Operations.ERA, target=function_name))
    pass


def p_increment_argument_counter(p):
    'increment_argument_counter : '
    global argument_counter
    argument_counter += 1
    pass


def p_check_arg_count_type(p):
    # Check if param_counter is not greater than params list, check arg type, and get arg address or create one, add Param quad
    'check_arg_count_type : '
    global argument_counter
    arg_value = PilaOperandos.pop()
    arg_type = PTypes.pop()
    function_name = last_func_call[-1]

    # Get func_name scope_ref
    func_ref = get_func_ref(current_scope_ref, function_name)

    # Check if param list length is bigger than current argument counter
    params_list = funcsTable.dict[func_ref].params
    if (argument_counter >= len(params_list)):
        raise Exception(
            'Semantic error: Too many arguments in "%s" call.' % function_name)

    # Get param_name type by checking vars in current context
    param_type = funcsTable.dict[func_ref].vars[params_list[argument_counter]]['type']
    # Check if argument type is equal to parameter type
    if (arg_type != param_type):
        raise Exception('Semantic error: Argument in position "%s" type does not match parameter type in function "%s"' %
                        argument_counter + 1, function_name)

    # Temp param name
    argument_temp = f"${argument_counter}"
    # Debug quad list
    quadruple_name_list.append(
        Quadruple(Operations.PARAM, left=arg_value, target=argument_temp))
    # Addr quad list
    quadruple_address_list.append(Quadruple(Operations.PARAM, left=get_addr(
        arg_value, arg_type), target=funcsTable.dict[func_ref].vars[params_list[argument_counter]]['addr']))
    pass


def p_create_gosub_quad(p):
    # Add gosub quad, create return var
    'create_gosub_quad : '
    # Remove flase bottom
    POper.pop()

    # Check number of arguments is not less than params list
    function_name = last_func_call[-1]
    func_ref = get_func_ref(current_scope_ref, function_name)
    params_list = funcsTable.dict[func_ref].params

    global argument_counter
    if (argument_counter < len(params_list) - 1):
        raise Exception(
            'Semantic error: Too few arguments in "%s" call.' % function_name)

    # Reset argument counter
    argument_counter = 0

    # Get function_name scope ref
    function_ref = get_func_ref(current_scope_ref, function_name)

    # Get start_quad to create gosub target
    func_quad_start = funcsTable.dict[function_ref].quad_start

    # Debug quad list
    quadruple_name_list.append(
        Quadruple(Operations.GOSUB, function_name, target=func_quad_start))
    # Addr quad list
    quadruple_address_list.append(
        Quadruple(Operations.GOSUB, function_name, target=func_quad_start))

    if(len(POper) != 0 and funcsTable.dict[func_ref].return_type == types_map['void']):
        raise Exception(
            "Semantic error: Can't use void function as value.")

    if funcsTable.dict[func_ref].return_type != types_map['void']:
        # Handle return_value
        return_type = funcsTable.dict[function_ref].return_type

        return_var_name = f"${function_name}_return_value"

        PilaOperandos.append(return_var_name)
        PTypes.append(return_type)

        funcsTable.dict[current_scope_ref].add_variable(
            return_var_name, return_type, return_var_name)

    last_func_call.pop()
    pass


def p_validate_return(p):
    'validate_return :'
    aux_func_ref = current_scope_ref
    while aux_func_ref > -1:
        if funcsTable.dict[aux_func_ref].function_name:
            function_ref = aux_func_ref
            break
        else:
            aux_func_ref = funcsTable.dict[aux_func_ref].parent_ref

    if aux_func_ref == -1:
        # No function found for return statement
        raise Exception('Semantic error: Return is not inside a function.')

    function_name = funcsTable.dict[function_ref].function_name
    function_return_type = funcsTable.dict[function_ref].return_type
    return_var_name = f"${function_name}_return_value"

    # Check if return is inside void function
    if function_return_type == types_map['void']:
        raise Exception(
            'Semantic error: Return statement in void function "%s".' % function_name)

    return_value = PilaOperandos.pop()
    return_type = PTypes.pop()

    # Check if return type is equal to function return type
    if return_type != function_return_type:
        raise Exception('Semantic error: Returned value type does not match function return type in function "%s"' %
                        function_name)

    if(return_value != 1):
        return_var_name = f"${function_name}_return_value"

        # Add return quad
        quadruple_name_list.append(
            Quadruple(Operations.RETURN, left=get_addr(return_value, return_type), target=return_var_name))

        # Add return quad
        quadruple_address_list.append(Quadruple(Operations.RETURN, left=get_addr(return_value, return_type),
                                                target=return_var_name))
    global return_counter
    return_counter += 1
    pass


def p_add_operator_to_stack(p):
    # add operator symbol to stack
    'add_operator_to_stack : '
    POper.append(operations_map[get_last_token(p)])
    pass


def p_set_current_type(p):
    # change global current_type when you encounter float, string, bool, int
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
            'Semantic error: Variable "%s" already exists.' % var_name)
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
            'Semantic error: Variable "%s" does not exist.' % var_name)
    aux_scope_ref = current_scope_ref
    while aux_scope_ref > -1:
        if var_name in funcsTable.dict[aux_scope_ref].vars:
            if funcsTable.dict[aux_scope_ref].vars[var_name]['d1']:
                raise Exception(
                    'Semantic error: Array "%s" is not indexed.' % var_name)
            global current_type
            # change current type if it exists
            current_type = funcsTable.dict[aux_scope_ref].vars[var_name]['type']
        aux_scope_ref = funcsTable.dict[aux_scope_ref].parent_ref
    pass


def p_init_array(p):
    'init_array : '
    # get array initial position from type stack/mem
    array_name = get_last_token(p)
    array_type = current_type
    if array_type != Types.INT_TYPE and array_type != Types.FLOAT_TYPE:
        raise Exception(
            'Semantic error: Array "%s" must be of type int or float.' % array_name)
    array_address = get_addr(array_name, array_type)
    # add to scope tree
    funcsTable.dict[current_scope_ref].add_variable(
        array_name, array_type, array_address)
    # add to last stack referenced
    global array_name_stack
    array_name_stack.append(array_name)
    pass


def p_init_array_size(p):
    'init_array_size : '
    # add size to size stack
    array_size = get_last_token(p)
    array_size_stack.append(array_size)
    pass


def reserve_array_mem(arr_size, arr_type):
    if(arr_type == Types.INT_TYPE):
        global last_int_address
        check_out_of_mem(last_int_address + arr_size - 1, DIR_INT_MAX)
        last_int_address += arr_size - 1
    elif(arr_type == Types.FLOAT_TYPE):
        global last_float_address
        check_out_of_mem(last_float_address + arr_size - 1, DIR_FLOAT_MAX)
        last_float_address += arr_size - 1
    else:
        raise Exception('Semantic error: Out of memory for array declaration.')


def p_init_array_variable(p):
    'init_array_variable : '
    # pop the size of the array, 'apartar' la memoria
    array_size = int(array_size_stack.pop())
    array_type = current_type
    reserve_array_mem(array_size, array_type)
    # Set size in scope tree
    last_array_name = array_name_stack.pop()
    funcsTable.dict[current_scope_ref].vars[last_array_name]['d1'] = array_size
    insert_constant(array_size, Types.INT_TYPE)
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


def p_add_int_type_to_stack(p):
    'add_int_type_to_stack : '
    token = get_last_token(p)
    insert_constant(token, Types.INT_TYPE)
    add_to_operand_type_stacks(token, Types.INT_TYPE)
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


def p_array_name_reference(p):
    'array_name_reference : '
    array_name = get_last_token(p)
    array_name_stack.append(array_name)
    pass


def p_array_reference_value(p):
    'array_reference_value : '
    # verify that array exists
    array_name = array_name_stack.pop()
    aux_scope_ref = current_scope_ref
    d1 = -1
    array_start_address = -1
    array_type = None
    while(aux_scope_ref > -1):
        scope_vars = funcsTable.dict[aux_scope_ref].vars
        if array_name in scope_vars:
            # get d1
            d1 = scope_vars[array_name]['d1']
            if d1 == None:
                raise Exception(
                    'Semantic error: avg() function only accepts arrays.')
            # get initial addr
            array_start_address = scope_vars[array_name]['addr']
            # get array type
            array_type = funcsTable.dict[aux_scope_ref].vars[array_name]['type']
            break
        if aux_scope_ref == 0:
            raise Exception(
                'Semantic error: Variable array "%s" does not exist.' % array_name)
        aux_scope_ref = funcsTable.dict[aux_scope_ref].parent_ref

    # VER Quad
    s1 = PilaOperandos.pop()
    s1_type = PTypes.pop()

    if s1_type != Types.INT_TYPE:
        raise Exception(
            'Semantic error: Tried to access array "%s" with a non INT value.' % array_name)

    # Add to debug quad
    quadruple_name_list.append(
        Quadruple(Operations.VER, 0, d1, s1))

    # Add to addr quad
    quadruple_address_list.append(
        Quadruple(Operations.VER, 0, d1, get_addr(s1, array_type)))

    # Get address with QUAD
    virtual_var_name = create_temp_virtual_var()
    virtual_var_address = get_addr(virtual_var_name, array_type)

    virtual_var_list.append(virtual_var_address)

    funcsTable.dict[current_scope_ref].add_variable(
        virtual_var_name, array_type, virtual_var_address)

    # Add to debug quad
    quadruple_name_list.append(
        Quadruple(Operations.PLUSV, array_start_address, s1, virtual_var_name))

    # Add to addr quad
    quadruple_address_list.append(Quadruple(Operations.PLUSV, array_start_address, get_addr(
        s1, Types.INT_TYPE), virtual_var_address))

    PilaOperandos.append(virtual_var_name)
    PTypes.append(array_type)
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
        raise Exception('Semantic error: Condition must be boolean.')

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


def p_goto_return_position(p):
    'goto_return_position : '
    PJumps.append(len(quadruple_address_list))
    pass


def p_return_end_jump_position(p):
    'return_end_jump_position : '
    end = PJumps.pop()
    return_jump = PJumps.pop()

    # Debug quad list
    quadruple_name_list.append(Quadruple(Operations.GOTO, target=return_jump))

    # Addr quad list
    quadruple_address_list.append(
        Quadruple(Operations.GOTO, target=return_jump))

    # Debug quad list
    quadruple_name_list[end].target = len(quadruple_address_list)
    # Addr quad list
    quadruple_address_list[end].target = len(quadruple_address_list)
    pass


def p_goto_main(p):
    'goto_main : '
    quadruple_name_list.append(Quadruple(Operations.GOTO))
    quadruple_address_list.append(Quadruple(Operations.GOTO))
    PJumps.append(len(quadruple_address_list) - 1)
    pass


def p_main_quad(p):
    'main_quad : '
    goto_main = PJumps.pop()
    quadruple_address_list[goto_main].target = len(quadruple_address_list)
    quadruple_name_list[goto_main].target = len(quadruple_address_list)
    quadruple_name_list.append(Quadruple(Operations.MAIN))
    quadruple_address_list.append(Quadruple(Operations.MAIN))
    pass


def p_check_absolute_argument_value(p):
    'check_absolute_argument_value : '
    value_name = PilaOperandos.pop()
    value_type = PTypes.pop()
    if value_type != Types.FLOAT_TYPE and value_type != Types.INT_TYPE:
        raise Exception(
            'Semantic error: absolute() function only accepts floats or ints.')

    # Temp variable
    result = create_temp_var()
    # Add to addr quad
    result_addr = get_addr(result, value_type)

    PilaOperandos.append(result)
    PTypes.append(value_type)

    # Append temp variable to scope
    funcsTable.dict[current_scope_ref].add_variable(
        result, value_type, result_addr)

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.ABSOLUTE, value_name, target=result))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.ABSOLUTE, get_addr(value_name, value_type), target=result_addr))
    pass


def p_check_trunc_argument_value(p):
    'check_trunc_argument_value : '
    value_name = PilaOperandos.pop()
    value_type = PTypes.pop()
    if value_type != Types.FLOAT_TYPE and value_type != Types.INT_TYPE:
        raise Exception(
            'Semantic error: trunc() function only accepts floats or ints.')

    # Temp variable
    result = create_temp_var()
    # Add to addr quad
    result_addr = get_addr(result, value_type)

    PilaOperandos.append(result)
    PTypes.append(value_type)

    # Append temp variable to scope
    funcsTable.dict[current_scope_ref].add_variable(
        result, value_type, result_addr)

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.TRUNC, value_name, target=result))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.TRUNC, get_addr(value_name, value_type), target=result_addr))
    pass


def p_check_sqrt_argument_value(p):
    'check_sqrt_argument_value : '
    value_name = PilaOperandos.pop()
    value_type = PTypes.pop()
    if value_type != Types.FLOAT_TYPE and value_type != Types.INT_TYPE:
        raise Exception(
            'Semantic error: sqrt() function only accepts floats or ints.')

    # Temp variable
    result = create_temp_var()
    # Add to addr quad
    result_addr = get_addr(result, value_type)

    PilaOperandos.append(result)
    PTypes.append(value_type)

    # Append temp variable to scope
    funcsTable.dict[current_scope_ref].add_variable(
        result, value_type, result_addr)

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.SQRT, value_name, target=result))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.SQRT, get_addr(value_name, value_type), target=result_addr))
    pass


def p_substr_quad(p):
    'substr_quad : '
    # End index parameter
    end_index = PilaOperandos.pop()
    end_index_type = PTypes.pop()
    if end_index_type != Types.INT_TYPE:
        raise Exception(
            'Semantic error: substr() last parameter is not an int.')

    start_index = PilaOperandos.pop()
    start_index_type = PTypes.pop()
    if start_index_type != Types.INT_TYPE:
        raise Exception(
            'Semantic error: substr() second parameter is not an int.')

    string_x = PilaOperandos.pop()
    string_x_type = PTypes.pop()
    if string_x_type != Types.STRING_TYPE:
        raise Exception(
            'Semantic error: substr() first parameter is not a string.')

     # Temp variable
    result = create_temp_var()
    # Add to addr quad
    result_addr = get_addr(result, string_x_type)

    PilaOperandos.append(result)
    PTypes.append(string_x_type)

    # Append temp variable to scope
    funcsTable.dict[current_scope_ref].add_variable(
        result, string_x_type, result_addr)

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.SUBSTR, string_x, [get_addr(start_index, string_x_type), get_addr(end_index, string_x_type)], target=result))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.SUBSTR, get_addr(string_x, string_x_type), [get_addr(start_index, string_x_type), get_addr(end_index, string_x_type)], target=result_addr))

    pass


def p_check_to_lower_argument_value(p):
    'check_to_lower_argument_value : '
    value_name = PilaOperandos.pop()
    value_type = PTypes.pop()

    if value_type != Types.STRING_TYPE:
        raise Exception(
            'Semantic error: toLower() function only accepts strings.')

    # Temp variable
    result = create_temp_var()
    # Add to addr quad
    result_addr = get_addr(result, value_type)

    PilaOperandos.append(result)
    PTypes.append(value_type)

    # Append temp variable to scope
    funcsTable.dict[current_scope_ref].add_variable(
        result, value_type, result_addr)

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.TOLOWER, value_name, target=result))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.TOLOWER, get_addr(value_name, value_type), target=result_addr))

    pass


def p_check_to_upper_argument_value(p):
    'check_to_upper_argument_value : '
    value_name = PilaOperandos.pop()
    value_type = PTypes.pop()

    if value_type != Types.STRING_TYPE:
        raise Exception(
            'Semantic error: toUpper() function only accepts strings.')

    # Temp variable
    result = create_temp_var()
    # Add to addr quad
    result_addr = get_addr(result, value_type)

    PilaOperandos.append(result)
    PTypes.append(value_type)

    # Append temp variable to scope
    funcsTable.dict[current_scope_ref].add_variable(
        result, value_type, result_addr)

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.TOUPPER, value_name, target=result))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.TOUPPER, get_addr(value_name, value_type), target=result_addr))

    pass


def p_check_avg_argument_value(p):
    'check_avg_argument_value : '
    array_name = PilaOperandos.pop()
    value_type = PTypes.pop()

    if value_type != Types.INT_TYPE and value_type != Types.FLOAT_TYPE:
        raise Exception(
            'Semantic error: avg() function only accepts arrays of ints or floats.')

    d1 = -1
    array_start_address = -1

    # Ger scope ref of array
    aux_scope_ref = current_scope_ref
    while(aux_scope_ref > -1):
        scope_vars = funcsTable.dict[aux_scope_ref].vars
        if array_name in scope_vars:
            # get d1
            d1 = scope_vars[array_name]['d1']
            if d1 == None:
                raise Exception(
                    'Semantic error: avg() function only accepts arrays.')
            # get initial addr
            array_start_address = scope_vars[array_name]['addr']
            break
        if aux_scope_ref == 0:
            raise Exception(
                'Semantic error: Variable array "%s" does not exist.' % array_name)
        aux_scope_ref = funcsTable.dict[aux_scope_ref].parent_ref

    # Temp variable
    result = create_temp_var()
    # Add to addr quad
    result_addr = get_addr(result, value_type)

    PilaOperandos.append(result)
    PTypes.append(value_type)

    # Append temp variable to scope
    funcsTable.dict[current_scope_ref].add_variable(
        result, value_type, result_addr)

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.AVG, array_name, array_start_address + d1 - 1, target=result))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.AVG, array_start_address, array_start_address + d1 - 1, target=result_addr))

    pass


def p_check_sum_argument_value(p):
    'check_sum_argument_value : '
    array_name = PilaOperandos.pop()
    value_type = PTypes.pop()

    if value_type != Types.INT_TYPE and value_type != Types.FLOAT_TYPE:
        raise Exception(
            'Semantic error: sum() function only accepts arrays of ints or floats.')

    d1 = -1
    array_start_address = -1

    # Ger scope ref of array
    aux_scope_ref = current_scope_ref
    while(aux_scope_ref > -1):
        scope_vars = funcsTable.dict[aux_scope_ref].vars
        if array_name in scope_vars:
            # get d1
            d1 = scope_vars[array_name]['d1']
            if d1 == None:
                raise Exception(
                    'Semantic error: sum() function only accepts arrays.')
            # get initial addr
            array_start_address = scope_vars[array_name]['addr']
            break
        if aux_scope_ref == 0:
            raise Exception(
                'Semantic error: Variable array "%s" does not exist.' % array_name)
        aux_scope_ref = funcsTable.dict[aux_scope_ref].parent_ref

    # Temp variable
    result = create_temp_var()
    # Add to addr quad
    result_addr = get_addr(result, value_type)

    PilaOperandos.append(result)
    PTypes.append(value_type)

    # Append temp variable to scope
    funcsTable.dict[current_scope_ref].add_variable(
        result, value_type, result_addr)

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.SUM, array_name, array_start_address + d1 - 1, target=result))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.SUM, array_start_address, array_start_address + d1 - 1, target=result_addr))

    pass


def p_check_max_argument_value(p):
    'check_max_argument_value : '
    array_name = PilaOperandos.pop()
    value_type = PTypes.pop()

    if value_type != Types.INT_TYPE and value_type != Types.FLOAT_TYPE:
        raise Exception(
            'Semantic error: max() function only accepts arrays of ints or floats.')

    d1 = -1
    array_start_address = -1

    # Ger scope ref of array
    aux_scope_ref = current_scope_ref
    while(aux_scope_ref > -1):
        scope_vars = funcsTable.dict[aux_scope_ref].vars
        if array_name in scope_vars:
            # get d1
            d1 = scope_vars[array_name]['d1']
            if d1 == None:
                raise Exception(
                    'Semantic error: max() function only accepts arrays.')
            # get initial addr
            array_start_address = scope_vars[array_name]['addr']
            break
        if aux_scope_ref == 0:
            raise Exception(
                'Semantic error: Variable array "%s" does not exist.' % array_name)
        aux_scope_ref = funcsTable.dict[aux_scope_ref].parent_ref

    # Temp variable
    result = create_temp_var()
    # Add to addr quad
    result_addr = get_addr(result, value_type)

    PilaOperandos.append(result)
    PTypes.append(value_type)

    # Append temp variable to scope
    funcsTable.dict[current_scope_ref].add_variable(
        result, value_type, result_addr)

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.MAX, array_name, array_start_address + d1 - 1, target=result))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.MAX, array_start_address, array_start_address + d1 - 1, target=result_addr))

    pass


def p_check_min_argument_value(p):
    'check_min_argument_value : '
    array_name = PilaOperandos.pop()
    value_type = PTypes.pop()

    if value_type != Types.INT_TYPE and value_type != Types.FLOAT_TYPE:
        raise Exception(
            'Semantic error: min() function only accepts arrays of ints or floats.')

    d1 = -1
    array_start_address = -1

    # Ger scope ref of array
    aux_scope_ref = current_scope_ref
    while(aux_scope_ref > -1):
        scope_vars = funcsTable.dict[aux_scope_ref].vars
        if array_name in scope_vars:
            # get d1
            d1 = scope_vars[array_name]['d1']
            if d1 == None:
                raise Exception(
                    'Semantic error: min() function only accepts arrays.')
            # get initial addr
            array_start_address = scope_vars[array_name]['addr']
            break
        if aux_scope_ref == 0:
            raise Exception(
                'Semantic error: Variable array "%s" does not exist.' % array_name)
        aux_scope_ref = funcsTable.dict[aux_scope_ref].parent_ref

    # Temp variable
    result = create_temp_var()
    # Add to addr quad
    result_addr = get_addr(result, value_type)

    PilaOperandos.append(result)
    PTypes.append(value_type)

    # Append temp variable to scope
    funcsTable.dict[current_scope_ref].add_variable(
        result, value_type, result_addr)

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.MIN, array_name, array_start_address + d1 - 1, target=result))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.MIN, array_start_address, array_start_address + d1 - 1, target=result_addr))

    pass


def p_check_len_argument_value(p):
    'check_len_argument_value : '
    array_name = PilaOperandos.pop()
    value_type = PTypes.pop()

    d1 = -1
    array_start_address = -1

    # Ger scope ref of array
    aux_scope_ref = current_scope_ref
    while(aux_scope_ref > -1):
        scope_vars = funcsTable.dict[aux_scope_ref].vars
        if array_name in scope_vars:
            # get d1
            d1 = scope_vars[array_name]['d1']
            if d1 == None:
                raise Exception(
                    'Semantic error: len() function only accepts arrays.')
            # get initial addr
            array_start_address = scope_vars[array_name]['addr']
            break
        if aux_scope_ref == 0:
            raise Exception(
                'Semantic error: Variable array "%s" does not exist.' % array_name)
        aux_scope_ref = funcsTable.dict[aux_scope_ref].parent_ref

    # Temp variable
    result = create_temp_var()
    # Add to addr quad
    result_addr = get_addr(result, value_type)

    PilaOperandos.append(result)
    PTypes.append(value_type)

    # Append temp variable to scope
    funcsTable.dict[current_scope_ref].add_variable(
        result, value_type, result_addr)

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.LEN, array_name, array_start_address + d1 - 1, target=result))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.LEN, array_start_address, array_start_address + d1 - 1, target=result_addr))

    pass


def p_check_sort_argument_value(p):
    'check_sort_argument_value : '
    sort_direction = POper.pop().value
    array_name = PilaOperandos.pop()
    value_type = PTypes.pop()

    if value_type != Types.INT_TYPE and value_type != Types.FLOAT_TYPE:
        raise Exception(
            'Semantic error: sort() function only accepts arrays of ints or floats.')

    d1 = -1
    array_start_address = -1

    # Ger scope ref of array
    aux_scope_ref = current_scope_ref
    while(aux_scope_ref > -1):
        scope_vars = funcsTable.dict[aux_scope_ref].vars
        if array_name in scope_vars:
            # get d1
            d1 = scope_vars[array_name]['d1']
            if d1 == None:
                raise Exception(
                    'Semantic error: sort() function only accepts arrays.')
            # get initial addr
            array_start_address = scope_vars[array_name]['addr']
            break
        if aux_scope_ref == 0:
            raise Exception(
                'Semantic error: Variable array "%s" does not exist.' % array_name)
        aux_scope_ref = funcsTable.dict[aux_scope_ref].parent_ref

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.SORT, array_name, array_start_address + d1 - 1, target=sort_direction))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.SORT, array_start_address, array_start_address + d1 - 1, target=sort_direction))

    pass


def p_check_find_argument_value(p):
    'check_find_argument_value : '
    value_to_find = PilaOperandos.pop()
    value_to_find_type = PTypes.pop()

    array_name = PilaOperandos.pop()
    value_type = PTypes.pop()

    if value_type != Types.INT_TYPE and value_type != Types.FLOAT_TYPE:
        raise Exception(
            'Semantic error: find() function only accepts arrays of ints or floats.')

    if value_to_find_type != value_type:
        raise Exception(
            'Semantic error: find() function only accepts the same type of array and item.')

    d1 = -1
    array_start_address = -1

    # Ger scope ref of array
    aux_scope_ref = current_scope_ref
    while(aux_scope_ref > -1):
        scope_vars = funcsTable.dict[aux_scope_ref].vars
        if array_name in scope_vars:
            # get d1
            d1 = scope_vars[array_name]['d1']
            if d1 == None:
                raise Exception(
                    'Semantic error: find() function only accepts arrays.')
            # get initial addr
            array_start_address = scope_vars[array_name]['addr']
            break
        if aux_scope_ref == 0:
            raise Exception(
                'Semantic error: Variable array "%s" does not exist.' % array_name)
        aux_scope_ref = funcsTable.dict[aux_scope_ref].parent_ref

    # Temp variable
    result = create_temp_var()
    # Add to addr quad
    result_addr = get_addr(result, Types.INT_TYPE)

    PilaOperandos.append(result)
    PTypes.append(Types.INT_TYPE)

    # Append temp variable to scope
    funcsTable.dict[current_scope_ref].add_variable(
        result, Types.INT_TYPE, result_addr)

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.FIND, array_name, [array_start_address + d1 - 1, value_to_find], target=result))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.FIND, array_start_address, [array_start_address + d1 - 1, get_addr(value_to_find, value_to_find_type)], target=result_addr))

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


def p_read_value(p):
    # Create read quadruple
    'read_value : '
    value_name = PilaOperandos.pop()
    value_type = PTypes.pop()

    # Debug Quad list
    quadruple_name_list.append(
        Quadruple(Operations.READ, value_type.value, target=value_name))
    # Addr Quad list
    quadruple_address_list.append(
        Quadruple(Operations.READ, value_type.value, target=get_addr(value_name, value_type)))

    pass


def p_end_program(p):
    'end_program : '
    quadruple_name_list.append(Quadruple(Operations.END))
    quadruple_address_list.append(Quadruple(Operations.END))
    pass


def p_program(p):
    '''program : PROGRAM ID SEMICOLON global_vars goto_main global_declaration main_declaration end_program'''
    pass


def p_global_vars(p):
    '''global_vars : global_vars global_vars_actions
    | empty'''
    pass


def p_global_vars_actions(p):
    '''global_vars_actions : declare_var
    | assign_statement'''
    pass


def p_global_declaration(p):
    '''global_declaration : global_declaration global_statement
    | empty'''
    pass


def p_global_statement(p):
    '''global_statement : declare_function
    | declare_function_void
    | print'''
    pass


def p_main_declaration(p):
    '''main_declaration : MAIN main_quad LPARENT RPARENT LBRACE new_scope statement_list RBRACE close_current_scope SEMICOLON'''
    pass


def p_statement_list(p):
    '''statement_list : statement_list statement
    | empty'''
    pass


def p_statement(p):
    '''statement : declare_var
    | assign_statement
    | function_call
    | if_condition
    | while_loop
    | return
    | read
    | sort_array
    | print'''
    pass


def p_declare_function(p):
    '''declare_function : FUNCTION ID new_function_scope LESSTHAN function_type GREATERTHAN LPARENT params RPARENT LBRACE function_start_quad statement_list return RBRACE endfunc_quad close_current_scope SEMICOLON'''
    pass


def p_declare_function_void(p):
    '''declare_function_void : FUNCTION ID new_function_scope LESSTHAN VOID_TYPE set_func_return_type GREATERTHAN LPARENT params RPARENT LBRACE function_start_quad statement_list RBRACE endfunc_quad close_current_scope SEMICOLON'''
    pass


def p_function_type(p):
    '''function_type : FLOAT_TYPE set_func_return_type
    | INT_TYPE set_func_return_type
    | STRING_TYPE set_func_return_type
    | BOOL_TYPE set_func_return_type'''
    pass


def p_params(p):
    '''params : param
    | param COMMA params
    '''
    pass


def p_param(p):
    '''
    param : var_type ID init_param
    '''
    pass


def p_function_call_value(p):
    '''function_call_value : ID init_func_call LPARENT arg_list RPARENT create_gosub_quad'''
    pass


def p_function_call(p):
    '''function_call : ID init_func_call LPARENT arg_list RPARENT create_gosub_quad SEMICOLON'''
    pass


def p_return(p):
    '''return : RETURN mega_expression validate_return SEMICOLON'''
    pass


def p_arg_list(p):
    '''
    arg_list : arg
    | arg COMMA increment_argument_counter arg_list
    '''
    pass


def p_arg(p):
    '''
    arg : mega_expression check_arg_count_type
    '''
    pass


def p_declare_var(p):
    '''declare_var : VAR var_type ID init_variable SEMICOLON
    | VAR var_type ID init_array LBRACKET INT init_array_size RBRACKET init_array_variable SEMICOLON
    '''
    pass


def p_assign_statement(p):
    '''assign_statement : VAR var_type ID init_variable add_id_type_to_stack EQUAL add_operator_to_stack mega_expression SEMICOLON
    | reference EQUAL add_operator_to_stack mega_expression SEMICOLON'''
    assign_var()
    pass


def p_var_type(p):
    '''var_type : FLOAT_TYPE set_current_type
    | INT_TYPE set_current_type
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
    | function_call_value
    | absolute_call_value
    | sqrt_call_value
    | trunc_call_value
    | substr_call_value
    | to_lower_call_value
    | to_upper_call_value
    | avg_call_value
    | find_array_value
    | max_array_value
    | min_array_value
    | sum_array_value
    | len_array_value
    '''
    pass


def p_literal(p):
    '''
    literal : FLOAT add_float_type_to_stack
    | INT add_int_type_to_stack
    | STRING add_string_type_stack
    | TRUE add_boolean_type_to_stack
    | FALSE add_boolean_type_to_stack
    '''
    pass


def p_reference(p):
    '''reference : ID check_variable_exists add_id_type_to_stack
    | array_reference'''
    pass


def p_array_reference(p):
    ''' array_reference : ID array_name_reference LBRACKET add_separator mega_expression RBRACKET remove_separator array_reference_value'''


def p_if_condition(p):
    '''
    if_condition : IF LPARENT mega_expression RPARENT LBRACE create_gotof_quad new_scope statement_list RBRACE close_current_scope else_condition goto_end_position
    '''
    pass


def p_else_condition(p):
    '''
    else_condition : ELSE goto_skip_else LBRACE new_scope statement_list RBRACE close_current_scope
    | empty
    '''
    pass


def p_while_loop(p):
    '''
    while_loop : WHILE goto_return_position LPARENT mega_expression RPARENT LBRACE create_gotof_quad new_scope statement_list RBRACE return_end_jump_position close_current_scope
    '''
    pass


def p_absolute_call_value(p):
    '''
    absolute_call_value : ABSOLUTE LPARENT mega_expression check_absolute_argument_value RPARENT
    '''
    pass


def p_sqrt_call_value(p):
    '''
    sqrt_call_value : SQRT LPARENT mega_expression check_sqrt_argument_value RPARENT
    '''
    pass


def p_trunc_call_value(p):
    '''
    trunc_call_value : TRUNC LPARENT mega_expression check_trunc_argument_value RPARENT
    '''
    pass


def p_to_lower_call_value(p):
    '''
    to_lower_call_value : TOLOWER LPARENT mega_expression check_to_lower_argument_value RPARENT
    '''
    pass


def p_to_upper_call_value(p):
    '''
    to_upper_call_value : TOUPPER LPARENT mega_expression check_to_upper_argument_value RPARENT
    '''
    pass


def p_substr_call_value(p):
    '''
    substr_call_value : SUBSTR LPARENT reference COMMA mega_expression COMMA mega_expression substr_quad RPARENT
    '''
    pass


def p_avg_call_value(p):
    '''
    avg_call_value : AVG LPARENT ID add_id_type_to_stack check_avg_argument_value RPARENT
    '''
    pass


def p_sort_array(p):
    '''
    sort_array : SORT LPARENT ID add_id_type_to_stack COMMA LESSTHAN add_operator_to_stack check_sort_argument_value RPARENT SEMICOLON
    | SORT LPARENT ID add_id_type_to_stack COMMA GREATERTHAN add_operator_to_stack check_sort_argument_value RPARENT SEMICOLON
    '''
    pass


def p_find_array_value(p):
    '''
    find_array_value : FIND LPARENT ID add_id_type_to_stack COMMA mega_expression check_find_argument_value RPARENT
    '''
    pass


def p_max_array_value(p):
    '''
    max_array_value : MAX LPARENT ID add_id_type_to_stack check_max_argument_value RPARENT
    '''
    pass


def p_min_array_value(p):
    '''
    min_array_value : MIN LPARENT ID add_id_type_to_stack check_min_argument_value RPARENT
    '''
    pass


def p_sum_array_value(p):
    '''
    sum_array_value : SUM LPARENT ID add_id_type_to_stack check_sum_argument_value RPARENT
    '''
    pass


def p_len_array_value(p):
    '''
    len_array_value : LEN LPARENT ID add_id_type_to_stack check_len_argument_value RPARENT
    '''
    pass


def p_print(p):
    '''
    print : PRINT LPARENT print_many RPARENT SEMICOLON
    '''
    pass


def p_print_many(p):
    '''
    print_many : mega_expression print_value
    | mega_expression print_value COMMA print_many
    '''
    pass


def p_read(p):
    '''
    read : READ LPARENT reference read_value RPARENT SEMICOLON
    '''
    pass


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    raise Exception('Syntax error in line: ' + str(p.lineno), p.value[0])


def print_funcsTable():
    print("--Scopes and Variables--")
    print(funcsTable)


def print_constantsTable():
    print("--Constants--")
    print(constants_table)


def print_quads():
    print("--Quads--")
    for index, quadRef in enumerate(quadruple_name_list):
        print(index, " ", quadRef)


def get_object_array():
    global quadruple_address_list
    # Create list of json objects only, remove classes
    object_array = []
    for quad in quadruple_address_list:
        object_array.append({
            'op_code': quad.op_code.value,
            'left': quad.left,
            'right': quad.right,
            'target': quad.target
        })
    return object_array


def contants_table_to_json():
    # Change type value from enum to string
    for key, value in constants_table.items():
        constants_table[key]['type'] = value['type'].value
    return constants_table


def create_scope_table():
    # Create scope table
    scope_table = {}
    for key, value in funcsTable.dict.items():
        for key_var, value_var in value.vars.items():
            value_var['type'] = value_var['type'].value
        if value.return_type:
            value.return_type = value.return_type.value
        scope_table[str(value.ref)] = {
            'ref': value.ref,
            'parent_ref': value.parent_ref,
            'params': value.params,
            'vars': value.vars,
            'functions': value.functions,
            'function_name': value.function_name,
            'quad_start': value.quad_start,
            'return_type': value.return_type,
        }
    return scope_table


def executeCompiler(filename):
    init_compiler()
    # Read the input file
    lines = []
    with open('./tests/' + filename) as f:
        lines = f.readlines()
    lex()
    # Build the parser
    parser = yacc(optimize=1, debug=False, write_tables=False)
    # Make a single string of the lines
    result = parser.parse(''.join(lines), debug=False)

    # Print the result
    print(result)


def executeCompilerCode(code):
    init_compiler()
    lex()
    # Build the parser
    parser = yacc(debug=True, write_tables=False)
    # Make a single string of the lines
    parser.parse(code, debug=False)
    return get_object_array(), contants_table_to_json(), create_scope_table(), virtual_var_list


if __name__ == "__main__":
    executeCompiler(sys.argv[1])
