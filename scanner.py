from token import Token
from exceptions import *
from tables import *

EOF = "\255"

class Scanner:
    def __init__(self, src: str):
        self.src = src + EOF
        self.cursor = 0 # 소스 내에서의 현재 커서의 위치
        self.line = 0 # 소스 내에서의 현재 라인의 위치. 에러 표시용
        self.line_cursor = 0 # 현재 라인에서의 커서의 상대 위치. 에러 표시용

    def is_octal(self, char: str):
        return char in "01234567"

    def is_hexa(self, char: str):
        return char in "ABCDEF"

    # 커서를 앞으로 한 칸 이동한다.
    def move_cursor(self):
        self.cursor += 1
        self.line_cursor += 1
    
    # \n를 만난 경우, 다음 줄로 이동하고 line_cursor 상대위치를 0으로 초기화
    def carriage_return(self):
        self.line_cursor = 0
        self.line += 1

    def get_token(self):
        token = ""
        state = 1

        while True:
            char = self.src[self.cursor]

            if state == 1:
                if char == EOF:
                    return None
                elif char.isspace():
                    if char == '\n':
                        self.carriage_return()
                    state = 1
                    self.move_cursor()
                elif char.isupper() or char == "_": # 대문자나 _ 로 시작하는 경우
                    state = 2
                    self.move_cursor()
                    token += char
                elif char.islower(): # 소문자로 시작하는 경우
                    state = 100
                    self.move_cursor()
                    token += char
                elif char.isnumeric() and char != "0":
                    state = 5
                    self.move_cursor()
                    token += char
                elif char == "0":
                    state = 6
                    self.move_cursor()
                    token += char
                elif char == "(":
                    state = 10
                    self.move_cursor()
                    token += char
                elif char == "/":
                    state = 13
                    self.move_cursor()
                    token += char
                elif char == "+":
                    state = 17
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "-":
                    state = 18
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "*":
                    state = 19
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "%":
                    state = 20
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "=":
                    state = 21
                    self.move_cursor()
                    token += char
                elif char == "!":
                    state = 23
                    self.move_cursor()
                    token += char
                elif char == "&":
                    state = 25
                    self.move_cursor()
                    token += char
                elif char == "|":
                    state = 27
                    self.move_cursor()
                    token += char
                elif char == "<":
                    state = 29
                    self.move_cursor()
                    token += char
                elif char == ">":
                    state = 31
                    self.move_cursor()
                    token += char
                elif char == "‘":
                    state = 33
                    self.move_cursor()
                    token += char
                elif char == "[":
                    state = 37
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "]":
                    state = 38
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "{":
                    state = 39
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "}":
                    state = 40
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == ")":
                    state = 41
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == ",":
                    state = 42
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == ";":
                    state = 43
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "’":
                    state = 44
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                else:
                    raise CharacterException(self)
            elif state == 2:
                if char.isalpha() or char.isdigit():
                    self.move_cursor()
                    token += char
                else:
                    # id 또는 keyword가 끝난 경우, keyword table 검색
                    if token in KEYWORD_TABLE:
                        state = 4
                        return Token(token, state)
                    # keyword가 아닌 경우, symbol table에 저장
                    else:
                        state = 3
                        # token이 테이블에 이미 있는 경우 넘어가고, 새로운 symbol인 경우 자신이 몇 번째인지 저장한다.
                        sym_table[token] = sym_table.get(token, len(sym_table))
                        return Token(token, state)
            elif state == 100:
                if char.islower():
                    self.move_cursor()
                    token += char
                else:
                    if token in KEYWORD_TABLE:
                        state = 4
                        return Token(token, state)
                    else:
                        raise KeywordNotFoundException(self)
            elif state == 5:
                if char.isnumeric():
                    state = 5
                    self.move_cursor()
                    token += char
                elif char == ".":
                    state = 51
                    self.move_cursor()
                    token += char
                elif char in "eE":
                    state = 53
                    self.move_cursor()
                    token += char
                else:
                    return Token(token, state)
            elif state == 51:
                if char.isdigit():
                    state = 52
                    self.move_cursor()
                    token += char
                else:
                    raise FloatException(self)
            elif state == 52:
                if char.isdigit():
                    state = 52
                    self.move_cursor()
                    token += char
                elif char in "eE":
                    state = 53
                    self.move_cursor()
                    token += char
                else:
                    return Token(token, state)
            elif state == 53:
                if char in "+-":
                    state = 54
                    self.move_cursor()
                    token += char
                else:
                    raise FloatException(self)
            elif state == 54:
                if char.isdigit():
                    state = 55
                    self.move_cursor()
                    token += char
                else:
                    raise FloatException(self)
            elif state == 55:
                if char.isdigit():
                    state = 55
                    self.move_cursor()
                    token += char
                else:
                    return Token(token, state)
            elif state == 6:
                if self.is_octal(char):
                    state = 7
                    self.move_cursor()
                    token += char
                elif char in "xX":
                    state = 8
                    self.move_cursor()
                    token += char
                # 8, 9 나오는 경우
                elif char in "89":
                    raise OctalException(self)
                else:
                    return Token(token, state)
            elif state == 7:
                if self.is_octal(char):
                    state = 7
                    self.move_cursor()
                    token += char
                else:
                    return Token(token, state)
            elif state == 8:
                if self.is_hexa(char) or char.isdigit():
                    state = 9
                    self.move_cursor()
                    token += char
                else:
                    raise HexException(self)
            elif state == 9:
                if self.is_hexa(char) or char.isdigit():
                    state = 9
                    self.move_cursor()
                    token += char
                else:
                    return Token(token, state)
            elif state == 10:
                if char == "*":
                    state = 11
                    self.move_cursor()
                    token += char
                else:
                    return Token(token, state)
            elif state == 11:
                if char != "*":
                    state = 11
                    self.move_cursor()
                    token += char
                else:
                    state = 12
                    self.move_cursor()
                    token += char
            elif state == 12:
                if char == "*":
                    state = 12
                    self.move_cursor()
                    token += char
                elif char == ")":
                    state = 1
                    self.move_cursor()
                    token = "" # 블럭 주석이 종료되면 쌓아두었던 주석을 지운다.
                else:
                    state = 11
                    self.move_cursor()
                    token += char
            elif state == 13:
                if char == "/":
                    state = 14
                    self.move_cursor()
                    token += char
                else:
                    return Token(token, state)
            elif state == 14:
                if char == "\n":
                    state = 1
                    self.move_cursor()
                    self.carriage_return()
                    token = "" # 라인 주석이 종료되면 쌓아두었던 주석을 지운다.
                elif char == EOF: # 라인 주석이 파일의 끝까지 있는 경우 state 1로 가서 처리
                    state = 1
                else:
                    state = 14
                    self.move_cursor()
                    token += char
            elif state == 21:
                if char == "=":
                    state = 22
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    return Token(token, state)
            elif state == 23:
                if char == "=":
                    state = 24
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    return Token(token, state)
            elif state == 25:
                if char == "&":
                    state = 26
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    raise OperatorException("&&", self)
            elif state == 27:
                if char == "|":
                    state = 28
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    raise OperatorException("||", self)
            elif state == 29:
                if char == "=":
                    state = 30
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    return Token(token, state)
            elif state == 31:
                if char == "=":
                    state = 31
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    return Token(token, state)
            elif state == 33:
                if char.isdigit():
                    state = 34
                    token += char
                    self.move_cursor()
                elif char.isalpha():
                    state = 35
                    token += char
                    self.move_cursor()                    
                else:
                    return Token(token, state)
            elif state == 34:
                if char.isdigit():
                    state = 34
                    token += char
                    self.move_cursor()
                elif char == "’":
                    state = 36
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    raise ConstException(0, self)
            elif state == 35:
                if char.isalpha():
                    state = 35
                    token += char
                    self.move_cursor()
                elif char == "’":
                    state = 36
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    raise ConstException(1, self)
