from enum import Enum

class TokenID(Enum):
    ID = 3
    CONSTANT = 4
    DEC = 5
    OCT = 6
    HEX = 7
    FLOAT = 9
    PLUS = 10
    MINUS = 11
    MUL = 12
    DIV = 13
    MOD = 14
    ASSIGN = 15
    EQUAL = 19
    NOT = 16
    AND = 17
    OR = 18
    NOTEQ = 20
    LT = 21
    GT = 22
    LE = 23
    GE = 25
    OPEN_BRACKET = 30
    CLOSE_BRACKET = 31
    OPEN_BRACE = 32
    CLOSE_BRACE = 33
    OPEN_PARENTHESIS = 34
    CLOSE_PARENTHESIS = 35
    COMMA = 36
    SEMI = 37
    OPEN_QUOTE = 38
    CLOSE_QUOTE = 39
    CONST = 43
    ELSE = 46
    IF = 40
    INT = 44
    CHAR = 51
    KEYWORD_FLOAT = 45
    RETURN = 47
    VOID = 48
    WHILE = 41
    FOR = 42
    BREAK = 49
    CONTINUE = 50

KEYWORD_TABLE = {
    "const": TokenID.CONST,
    "else": TokenID.ELSE,
    "if": TokenID.IF,
    "int": TokenID.INT,
    "char": TokenID.CHAR,
    "float": TokenID.KEYWORD_FLOAT,
    "return": TokenID.RETURN,
    "void": TokenID.VOID,
    "while": TokenID.WHILE,
    "for": TokenID.FOR,
    "break": TokenID.BREAK,
    "continue": TokenID.CONTINUE,
}
sym_table = dict()