# 
class ScannerException(Exception):
    def __init__(self, msg, cursor):
        super().__init__(msg + f"\n--- 오류 위치: {cursor}번 째 문자")

class CharacterException(ScannerException):
    def __init__(self, cursor):
        super().__init__("해당 문자로 시작할 수 없습니다.", cursor)

class KeywordNotFoundException(ScannerException):
    def __init__(self, cursor):
        super().__init__("keyword table에서 해당 예약어를 찾을 수 없습니다.", cursor)

class FloatException(ScannerException):
    def __init__(self, cursor):
        super().__init__("올바르지 않은 실수 형식입니다.", cursor)

class OctalException(ScannerException):
    def __init__(self, cursor):
        super().__init__("올바르지 않은 8진수 형식입니다.", cursor)

class HexException(ScannerException):
    def __init__(self, cursor):
        super().__init__("올바르지 않은 16진수 형식입니다.", cursor)

class OperatorException(ScannerException):
    def __init__(self, operator, cursor):
        super().__init__(f"올바르지 않은 연산자: {operator}을 쓰려고 하셨습니까?.", cursor)

class ConstException(ScannerException):
    def __init__(self, type, cursor):
        type_str = "숫자" if type == 0 else "문자"
        super().__init__(f"올바르지 않은 {type_str} 상수입니다.", cursor)
    