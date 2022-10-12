from collections import defaultdict
from enum import Enum


class Types(Enum):
    FLOAT_TYPE = 'float'
    BOOL_TYPE = 'bool'
    STRING_TYPE = 'string'
    VOID = 'void'


class Operations(Enum):
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'
    EQUAL = '='
    LESSTHAN = '<'
    GREATERTHAN = '>'
    EQUALEQUAL = '=='
    NOTEQUAL = '!='
    LESSTHANOREQUAL = '<='
    GREATERTHANOREQUAL = '>='
    GOTO = 'goto'
    GOTOF = 'gotoF'
    GOSUB = 'gosub'
    ERA = 'era'
    ENDFUNC = 'endFunc'
    START = 'start'
    END = 'end'
    PARAM = 'param'
    RETURN = 'return'
    PRINT = 'print'
    MAIN = 'main'


sem_cube = defaultdict(
    lambda: defaultdict(lambda: defaultdict(lambda: None)))

sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.GREATERTHANOREQUAL] = Types.BOOL_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.GREATERTHAN] = Types.BOOL_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.EQUALEQUAL] = Types.BOOL_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.LESSTHAN] = Types.BOOL_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.MINUS] = Types.FLOAT_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.NOTEQUAL] = Types.BOOL_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.LESSTHANOREQUAL] = Types.BOOL_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.TIMES] = Types.FLOAT_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.PLUS] = Types.FLOAT_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.DIVIDE] = Types.FLOAT_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.EQUAL] = Types.FLOAT_TYPE

sem_cube[Types.BOOL_TYPE][Types.BOOL_TYPE][Operations.EQUAL] = Types.BOOL_TYPE
sem_cube[Types.BOOL_TYPE][Types.BOOL_TYPE][Operations.EQUALEQUAL] = Types.BOOL_TYPE
sem_cube[Types.BOOL_TYPE][Types.BOOL_TYPE][Operations.LESSTHAN] = Types.BOOL_TYPE
sem_cube[Types.BOOL_TYPE][Types.BOOL_TYPE][Operations.NOTEQUAL] = Types.BOOL_TYPE
sem_cube[Types.BOOL_TYPE][Types.BOOL_TYPE][Operations.GREATERTHAN] = Types.BOOL_TYPE
sem_cube[Types.BOOL_TYPE][Types.BOOL_TYPE][Operations.LESSTHANOREQUAL] = Types.BOOL_TYPE
sem_cube[Types.BOOL_TYPE][Types.BOOL_TYPE][Operations.GREATERTHANOREQUAL] = Types.BOOL_TYPE

sem_cube[Types.STRING_TYPE][Types.STRING_TYPE][Operations.PLUS] = Types.STRING_TYPE
sem_cube[Types.STRING_TYPE][Types.STRING_TYPE][Operations.EQUAL] = Types.STRING_TYPE
