from tables import *
from enum import Enum

class TokenID(Enum):
    ID = 3
    PLUS = 10
    MINUS = 11
    MUL = 12
    DIV = 13
    OPEN_PARENTHESIS = 34
    CLOSE_PARENTHESIS = 35

class Token:
    def __init__(self, token, state):
        self.token = token
        self.state = state
    
    # 토큰의 accept state를 기반으로 아이디를 리턴한다.
    def get_id(self):
        if self.state == 3: # 식별자
            return TokenID.ID
        elif self.state == 4: # 예약어인 경우 keyword table 참조
            return KEYWORD_TABLE[self.token]
        elif self.state == 5: # 10진수
            return 5
        elif self.state == 52: # 123.123 형태의 실수
            return 9
        elif self.state == 55: # 123.123e-2 형태의 실수
            return 9
        elif self.state == 6: # 그냥 0은 8진수로 처리한다.
            return 6
        elif self.state == 7: # 8진수
            return 6
        elif self.state == 9: # 16진수
            return 7
        elif self.state == 10: # (
            return TokenID.OPEN_PARENTHESIS
        elif self.state == 13: # /
            return TokenID.DIV
        elif self.state == 17: # +
            return TokenID.PLUS
        elif self.state == 18: # -
            return TokenID.MINUS
        elif self.state == 19: # *
            return TokenID.MUL
        elif self.state == 20: # %
            return 14
        elif self.state == 21: # =
            return 15
        elif self.state == 22: # ==
            return 19
        elif self.state == 23: # !
            return 16
        elif self.state == 24: # !=
            return 20
        elif self.state == 26: # && 
            return 17
        elif self.state == 28: # ||
            return 18
        elif self.state == 29: # <
            return 21
        elif self.state == 30: # <=
            return 23
        elif self.state == 31: # >
            return 22
        elif self.state == 32: # >=
            return 25
        elif self.state == 33: # ‘ 여는 따옴표
            return 38
        elif self.state == 36: # 상수
            return 4
        elif self.state == 37: # [
            return 30
        elif self.state == 38: # ]
            return 31
        elif self.state == 39: # {
            return 32
        elif self.state == 40: # }
            return 33
        elif self.state == 41: # )
            return TokenID.CLOSE_PARENTHESIS
        elif self.state == 42: # ,
            return 36
        elif self.state == 43: # ;
            return 37
        elif self.state == 44: # ’ 닫는 따옴표
            return 39
    
    # 토큰의 값을 리턴한다.
    def get_value(self):
        if self.state == 3: # 식별자인 경우 symbol table 참조
            return sym_table[self.token]
        elif (self.state == 5 or  # 10진수
              self.state == 52 or # 실수
              self.state == 55 or # 실수
              self.state == 6 or  # 0
              self.state == 7 or  # 8진수
              self.state == 8 or  # 16진수
              self.state == 36):  # 상수
            return self.token
        else:
            return '-' # 그 외의 경우 토큰의 값은 없다.
    
    # 문자 리턴
    def get_char(self):
        return self.token

    # str() 메소드 오버라이드
    def __str__(self):
        return f'({self.get_id()}, {self.get_value()})  {self.token}'
