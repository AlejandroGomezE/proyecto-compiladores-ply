from collections import defaultdict
from enum import Enum


class Types(Enum):
    FLOAT_TYPE = 'float'
    INT_TYPE = 'int'
    BOOL_TYPE = 'bool'
    STRING_TYPE = 'string'
    VOID_TYPE = 'void'


class Operations(Enum):
    PLUS = '+'
    PLUSV = '+v'
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
    VER = 'ver'
    ENDFUNC = 'endFunc'
    START = 'start'
    END = 'end'
    PARAM = 'param'
    RETURN = 'return'
    PRINT = 'print'
    MAIN = 'main'
    ABSOLUTE = 'absolute'


sem_cube = defaultdict(
    lambda: defaultdict(lambda: defaultdict(lambda: None)))

sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.GREATERTHANOREQUAL] = Types.BOOL_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.GREATERTHAN] = Types.BOOL_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.EQUALEQUAL] = Types.BOOL_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.LESSTHAN] = Types.BOOL_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.NOTEQUAL] = Types.BOOL_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.LESSTHANOREQUAL] = Types.BOOL_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.MINUS] = Types.FLOAT_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.TIMES] = Types.FLOAT_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.PLUS] = Types.FLOAT_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.DIVIDE] = Types.FLOAT_TYPE
sem_cube[Types.FLOAT_TYPE][Types.FLOAT_TYPE][Operations.EQUAL] = Types.FLOAT_TYPE


sem_cube[Types.INT_TYPE][Types.FLOAT_TYPE][Operations.LESSTHAN] = sem_cube[Types.FLOAT_TYPE][Types.INT_TYPE][Operations.LESSTHAN] = Types.BOOL_TYPE
sem_cube[Types.INT_TYPE][Types.FLOAT_TYPE][Operations.GREATERTHAN] = sem_cube[Types.FLOAT_TYPE][Types.INT_TYPE][Operations.GREATERTHAN] = Types.BOOL_TYPE
sem_cube[Types.INT_TYPE][Types.FLOAT_TYPE][Operations.NOTEQUAL] = sem_cube[Types.FLOAT_TYPE][Types.INT_TYPE][Operations.NOTEQUAL] = Types.BOOL_TYPE
sem_cube[Types.INT_TYPE][Types.FLOAT_TYPE][Operations.EQUALEQUAL] = sem_cube[Types.FLOAT_TYPE][Types.INT_TYPE][Operations.EQUALEQUAL] = Types.BOOL_TYPE
sem_cube[Types.INT_TYPE][Types.FLOAT_TYPE][Operations.LESSTHANOREQUAL] = sem_cube[Types.FLOAT_TYPE][Types.INT_TYPE][Operations.LESSTHANOREQUAL] = Types.BOOL_TYPE
sem_cube[Types.INT_TYPE][Types.FLOAT_TYPE][Operations.GREATERTHANOREQUAL] = sem_cube[Types.FLOAT_TYPE][Types.INT_TYPE][Operations.GREATERTHANOREQUAL] = Types.BOOL_TYPE
sem_cube[Types.INT_TYPE][Types.FLOAT_TYPE][Operations.PLUS] = sem_cube[Types.FLOAT_TYPE][Types.INT_TYPE][Operations.PLUS] = Types.FLOAT_TYPE
sem_cube[Types.INT_TYPE][Types.FLOAT_TYPE][Operations.MINUS] = sem_cube[Types.FLOAT_TYPE][Types.INT_TYPE][Operations.MINUS] = Types.FLOAT_TYPE
sem_cube[Types.INT_TYPE][Types.FLOAT_TYPE][Operations.TIMES] = sem_cube[Types.FLOAT_TYPE][Types.INT_TYPE][Operations.TIMES] = Types.FLOAT_TYPE
sem_cube[Types.INT_TYPE][Types.FLOAT_TYPE][Operations.DIVIDE] = sem_cube[Types.FLOAT_TYPE][Types.INT_TYPE][Operations.DIVIDE] = Types.FLOAT_TYPE
sem_cube[Types.INT_TYPE][Types.FLOAT_TYPE][Operations.EQUAL] = Types.INT_TYPE
sem_cube[Types.FLOAT_TYPE][Types.INT_TYPE][Operations.EQUAL] = Types.FLOAT_TYPE


sem_cube[Types.INT_TYPE][Types.INT_TYPE][Operations.GREATERTHANOREQUAL] = Types.BOOL_TYPE
sem_cube[Types.INT_TYPE][Types.INT_TYPE][Operations.GREATERTHAN] = Types.BOOL_TYPE
sem_cube[Types.INT_TYPE][Types.INT_TYPE][Operations.EQUALEQUAL] = Types.BOOL_TYPE
sem_cube[Types.INT_TYPE][Types.INT_TYPE][Operations.LESSTHAN] = Types.BOOL_TYPE
sem_cube[Types.INT_TYPE][Types.INT_TYPE][Operations.NOTEQUAL] = Types.BOOL_TYPE
sem_cube[Types.INT_TYPE][Types.INT_TYPE][Operations.LESSTHANOREQUAL] = Types.BOOL_TYPE
sem_cube[Types.INT_TYPE][Types.INT_TYPE][Operations.MINUS] = Types.INT_TYPE
sem_cube[Types.INT_TYPE][Types.INT_TYPE][Operations.TIMES] = Types.INT_TYPE
sem_cube[Types.INT_TYPE][Types.INT_TYPE][Operations.PLUS] = Types.INT_TYPE
sem_cube[Types.INT_TYPE][Types.INT_TYPE][Operations.DIVIDE] = Types.INT_TYPE
sem_cube[Types.INT_TYPE][Types.INT_TYPE][Operations.EQUAL] = Types.INT_TYPE

sem_cube[Types.BOOL_TYPE][Types.BOOL_TYPE][Operations.EQUAL] = Types.BOOL_TYPE
sem_cube[Types.BOOL_TYPE][Types.BOOL_TYPE][Operations.EQUALEQUAL] = Types.BOOL_TYPE
sem_cube[Types.BOOL_TYPE][Types.BOOL_TYPE][Operations.NOTEQUAL] = Types.BOOL_TYPE

sem_cube[Types.STRING_TYPE][Types.STRING_TYPE][Operations.PLUS] = Types.STRING_TYPE
sem_cube[Types.STRING_TYPE][Types.STRING_TYPE][Operations.EQUAL] = Types.STRING_TYPE
