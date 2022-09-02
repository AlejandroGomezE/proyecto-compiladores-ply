# lextab.py. This file automatically created by PLY (version 3.11). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('BOOL_TYPE', 'DIVIDE', 'ELSE', 'EQUAL', 'EQUALEQUAL', 'FALSE', 'FLOAT', 'FLOAT_TYPE', 'GREATERTHAN', 'GREATERTHANOREQUAL', 'ID', 'IF', 'LBRACKET', 'LESSTHAN', 'LESSTHANOREQUAL', 'LPARENT', 'MAIN', 'MINUS', 'NOTEQUAL', 'PLUS', 'PRINT', 'PROGRAM', 'RBRACKET', 'RPARENT', 'SEMICOLON', 'STRING', 'STRING_TYPE', 'TIMES', 'TRUE', 'VAR'))
_lexreflags   = 64
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_ID>[a-zA-Z_][a-zA-Z_0-9]*)|(?P<t_newline>\\n+)|(?P<t_COMMENT>\\//.*)|(?P<t_FLOAT>((0|[1-9][0-9]*)\\.[0-9][0-9]*))|(?P<t_STRING>("(\\\\"|[^"])*"))|(?P<t_PLUS>\\+)|(?P<t_TIMES>\\*)|(?P<t_LPARENT>\\()|(?P<t_RPARENT>\\))|(?P<t_LBRACKET>\\{)|(?P<t_RBRACKET>\\})|(?P<t_EQUALEQUAL>==)|(?P<t_NOTEQUAL>!=)|(?P<t_LESSTHANOREQUAL><=)|(?P<t_GREATERTHANOREQUAL>>=)|(?P<t_MINUS>-)|(?P<t_DIVIDE>/)|(?P<t_COMMA>,)|(?P<t_SEMICOLON>;)|(?P<t_LESSTHAN><)|(?P<t_GREATERTHAN>>)|(?P<t_EQUAL>=)', [None, ('t_ID', 'ID'), ('t_newline', 'newline'), ('t_COMMENT', 'COMMENT'), (None, 'FLOAT'), None, None, (None, 'STRING'), None, None, (None, 'PLUS'), (None, 'TIMES'), (None, 'LPARENT'), (None, 'RPARENT'), (None, 'LBRACKET'), (None, 'RBRACKET'), (None, 'EQUALEQUAL'), (None, 'NOTEQUAL'), (None, 'LESSTHANOREQUAL'), (None, 'GREATERTHANOREQUAL'), (None, 'MINUS'), (None, 'DIVIDE'), (None, 'COMMA'), (None, 'SEMICOLON'), (None, 'LESSTHAN'), (None, 'GREATERTHAN'), (None, 'EQUAL')])]}
_lexstateignore = {'INITIAL': ' \t'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
