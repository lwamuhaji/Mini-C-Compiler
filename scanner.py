from mc_token import Token
from exceptions import *
from tables import *

EOF = "\255"

class Scanner:
    def __init__(self, src: str):
        self.src = src + EOF # 소스의 마지막에 EOF 문자를 추가한다.
        self.cursor = 0 # 소스 내에서의 현재 커서의 위치
        self.line = 0 # 소스 내에서의 현재 라인의 위치. 에러 표시용
        self.line_cursor = 0 # 현재 라인에서의 커서의 상대 위치. 에러 표시용

    def is_octal(self, char: str):
        return char in "01234567"

    def is_hexa(self, char: str):
        return char in "ABCDEFabcdef"

    # 커서를 앞으로 한 칸 이동한다.
    def move_cursor(self):
        self.cursor += 1
        self.line_cursor += 1
    
    # \n를 만난 경우, 다음 줄로 이동하고 line_cursor 상대위치를 0으로 초기화
    def carriage_return(self):
        self.line_cursor = 0
        self.line += 1

    # 소스파일로부터 토큰을 뽑아낸다.
    def get_token(self) -> Token:
        token = ""
        state = 1 # 시작 state

        while True:
            char = self.src[self.cursor] # 현재 커서 위치의 문자를 char에 저장

            if state == 1:
                if char == EOF: # 소스파일의 끝에 오면 None을 리턴한다.
                    return None
                elif char.isspace(): # whitespace인 경우 커서를 이동함
                    if char == '\n': # 다음 줄로 넘어가는 경우, 에러 표시용 line, line_cursor 계산
                        self.carriage_return()
                    state = 1
                    self.move_cursor()
                elif char.isupper() or char == "_": # 대문자나 _ 로 시작하는 경우: id or keyword
                    state = 2
                    self.move_cursor()
                    token += char
                elif char.islower(): # 소문자로 시작하는 경우: keyword
                    state = 100
                    self.move_cursor()
                    token += char
                elif char.isnumeric() and char != "0": # 0이 아닌 숫자인 경우: 10진수 또는 실수
                    state = 5
                    self.move_cursor()
                    token += char
                elif char == "0": # 0으로 시작하는 경우: octal
                    state = 6
                    self.move_cursor()
                    token += char
                elif char == "(": # ( 으로 시작하는 경우: ( 자체 또는 블록 주석의 시작일 수도 있다.
                    state = 10
                    self.move_cursor()
                    token += char
                elif char == "/": # / 로 시작하는 경우: / 자체 또는 라인 주석의 시작일 수도 있다.
                    state = 13
                    self.move_cursor()
                    token += char
                elif char == "+": # +=이나 ++같은 연산자는 존재하지 않기 때문에 +를 만나는 경우 accept state로 바로 이동(리턴)한다.
                    state = 17 # + state로 변경
                    self.move_cursor() # 커서 이동
                    token += char # +를 토큰에 추가함. token = '+'
                    return Token(token, state) # state와 token으로 Token 객체를 만들어 리턴
                elif char == "-": # -는 바로 리턴
                    state = 18
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "*": # *는 바로 리턴
                    state = 19
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "%": # %는 바로 리턴
                    state = 20
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "=": # = 또는 == 으로 전이할 수 있는 상태로 이동
                    state = 21
                    self.move_cursor()
                    token += char
                elif char == "!": # ! 또는 != 으로 전이할 수 있는 상태로 이동
                    state = 23
                    self.move_cursor()
                    token += char
                elif char == "&": # && 으로 전이 가능한 상태로 이동
                    state = 25
                    self.move_cursor()
                    token += char
                elif char == "|": # || 으로 전이 가능한 상태로 이동
                    state = 27
                    self.move_cursor()
                    token += char
                elif char == "<": # < 또는 <= 으로 전이할 수 있는 상태로 이동
                    state = 29
                    self.move_cursor()
                    token += char
                elif char == ">": # > 또는 >= 으로 전이할 수 있는 상태로 이동
                    state = 31
                    self.move_cursor()
                    token += char
                elif char == "‘": # ‘ 또는 상수로 전이할 수 있는 상태로 이동
                    state = 33
                    self.move_cursor()
                    token += char
                elif char == "[": # [는 바로 리턴
                    state = 37
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "]": # ]는 바로 리턴
                    state = 38
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "{": # {는 바로 리턴
                    state = 39
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "}": # }는 바로 리턴
                    state = 40
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == ")": # )는 바로 리턴
                    state = 41
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == ",": # ,는 바로 리턴
                    state = 42
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == ";": # ;는 바로 리턴
                    state = 43
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                elif char == "’": # ’는 바로 리턴
                    state = 44
                    self.move_cursor()
                    token += char
                    return Token(token, state)
                else:
                    raise CharacterException(self)
            elif state == 2: # id or keyword
                if char.isalpha() or char.isdigit(): # 다음 문자가 알파벳 또는 숫자인 경우 상태는 그대로이다.
                    self.move_cursor()
                    token += char
                else:
                    if token in KEYWORD_TABLE: # id 또는 keyword가 끝난 경우, keyword table 검색
                        state = 4
                        return Token(token, state)
                    else: # keyword가 아닌 경우, symbol table에 저장
                        state = 3
                        # token이 테이블에 이미 있는 경우 넘어가고, 새로운 symbol인 경우 자신이 몇 번째인지 저장한다.
                        sym_table[token] = sym_table.get(token, len(sym_table))
                        return Token(token, state)
            elif state == 100: # 소문자로 시작하는 경우: keyword
                if char.islower(): # 소문자가 나온 경우 상태는 그대로이다.
                    self.move_cursor()
                    token += char
                else: # 소문자 이외의 문자가 나온 경우 = keyword가 끝난 경우
                    if token in KEYWORD_TABLE: # keyword 테이블에서 검색해 존재하는 keyword이면 토큰리턴
                        state = 4
                        return Token(token, state)
                    else: # 존재하지 않는 keyword이면 에러 (왜냐하면 id는 소문자로 시작하지 않기 때문에, id가 될 수 없다.)
                        raise KeywordNotFoundException(self)
            elif state == 5: # 0이 아닌 숫자로 시작하는 경우
                if char.isnumeric(): # 숫자가 나오면 상태는 그대로
                    state = 5
                    self.move_cursor()
                    token += char
                elif char == ".": # . 이 나오면 불완전 실수 상태로 이동
                    state = 51
                    self.move_cursor()
                    token += char
                elif char in "eE": # e 또는 E가 나오면 불완전 실수 상태로 이동
                    state = 53
                    self.move_cursor()
                    token += char
                else: # 그게 아니라면 10진수로 판단, token 리턴
                    return Token(token, state)
            elif state == 51: # . 이 나온 실수 상태 ex) 123.
                if char.isdigit(): # 숫자가 나오면, 완전한 실수 상태로 이동
                    state = 52
                    self.move_cursor()
                    token += char
                else:
                    raise FloatException(self)
            elif state == 52: # 완전한 실수 상태 ex) 123.123
                if char.isdigit(): # 숫자가 나오면, 상태는 그대로이다.
                    state = 52
                    self.move_cursor()
                    token += char
                elif char in "eE": # 여기서 e 또는 E가 나오면 다시 불완전 실수 상태로 이동
                    state = 53
                    self.move_cursor()
                    token += char
                else:
                    return Token(token, state)
            elif state == 53: # 불완전 실수 상태 ex) 123.123E
                if char in "+-": # 여기서는 + 또는 - 나와야 한다. 그런 경우, 바로 아래 상태로 이동
                    state = 54
                    self.move_cursor()
                    token += char
                else: # +- 이외의 문자가 나오면 FloatException 발생
                    raise FloatException(self)
            elif state == 54: # 불완전 실수 상태 ex) 123.123E+
                if char.isdigit(): # 여기서 숫자가 나오면 완전한 실수 상태가 된다.
                    state = 55
                    self.move_cursor()
                    token += char
                else: # 숫자 이외의 문자가 나오면 FloatException 발생
                    raise FloatException(self)
            elif state == 55: # 완전한 실수 상태 ex) 123.123E+123
                if char.isdigit():
                    state = 55
                    self.move_cursor()
                    token += char
                else:
                    return Token(token, state)
            elif state == 6: # 0 하나 나온 상태
                if self.is_octal(char): # 0-7 이 나오면, 8진수 상태로 이동
                    state = 7
                    self.move_cursor()
                    token += char
                elif char in "xX": # x, X가 나오면 16진수 상태로 이동
                    state = 8
                    self.move_cursor()
                    token += char
                elif char in "89": # 8, 9가 나오면 에러 ex) 01239
                    raise OctalException(self)
                else:
                    return Token(token, state)
            elif state == 7: # 8진수 상태
                if self.is_octal(char):
                    state = 7
                    self.move_cursor()
                    token += char
                else:
                    return Token(token, state)
            elif state == 8: # 불완전 16진수 상태 ex) 0x
                if self.is_hexa(char) or char.isdigit():
                    state = 9
                    self.move_cursor()
                    token += char
                else:
                    raise HexException(self)
            elif state == 9: # 완전 16진수 상태 ex) 0xAF123
                if self.is_hexa(char) or char.isdigit():
                    state = 9
                    self.move_cursor()
                    token += char
                else:
                    return Token(token, state)
            elif state == 10: # ( 하나만 나온 상태
                if char == "*": # * 가 나오면, 주석 상태로 전이
                    state = 11
                    self.move_cursor()
                    token += char
                else:
                    return Token(token, state)
            elif state == 11: # 주석 상태 (*
                if char != "*":
                    state = 11
                    self.move_cursor()
                    token += char
                else:
                    state = 12
                    self.move_cursor()
                    token += char
            elif state == 12: # 주석 상태 (* 123 *
                if char == "*":
                    state = 12
                    self.move_cursor()
                    token += char
                elif char == ")": # (* 123 *)
                    state = 1
                    self.move_cursor()
                    token = "" # 블럭 주석이 종료되면 쌓아두었던 주석을 지운다.
                else:
                    state = 11
                    self.move_cursor()
                    token += char
            elif state == 13: # / 가 하나만 나온 상태
                if char == "/":
                    state = 14
                    self.move_cursor()
                    token += char
                else:
                    return Token(token, state)
            elif state == 14: # // 가 나온 주석 상태
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
            elif state == 21: # =이 하나만 나온 경우
                if char == "=":
                    state = 22
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    return Token(token, state)
            elif state == 23: # !가 나온 경우
                if char == "=":
                    state = 24
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    return Token(token, state)
            elif state == 25: # &이 나온 경우
                if char == "&":
                    state = 26
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    raise OperatorException("&&", self)
            elif state == 27: # # |이 나온 경우
                if char == "|":
                    state = 28
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    raise OperatorException("||", self)
            elif state == 29: # < 이 나온 경우
                if char == "=":
                    state = 30
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    return Token(token, state)
            elif state == 31: # > 이 나온 경우
                if char == "=":
                    state = 31
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    return Token(token, state)
            elif state == 33: # 여는 따옴표가 나온 경우
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
            elif state == 34: # 여는 따옴표 이후 숫자가 나온 경우: 숫자 상수
                if char.isdigit():
                    state = 34
                    token += char
                    self.move_cursor()
                elif char == "’": # 닫는 따옴표가 나온 경우: 상수 종료
                    state = 36
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    raise ConstException(0, self)
            elif state == 35: # 여는 따옴표 이후 문자가 나온 경우: 문자 상수
                if char.isalpha():
                    state = 35
                    token += char
                    self.move_cursor()
                elif char == "’": # 닫는 따옴표가 나온 경우: 상수 종료
                    state = 36
                    token += char
                    self.move_cursor()
                    return Token(token, state)
                else:
                    raise ConstException(1, self)
