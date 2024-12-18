# ScannerException: Exception을 상속받아 오류코드와 오류가 발생한 라인을 메시지로 설정한다. 
# 다른 Exception Class들은 ScannerException을 상속받아 구체적인 오류 케이스를 정의한다.

class ScannerException(Exception):
    def __init__(self, msg, scanner):
        # 오류가 시작된 라인의 시작 커서는 (전체커서-라인커서)
        start_cursor = scanner.cursor-scanner.line_cursor
        end_cursor = scanner.cursor
        # 오류가 발생한 라인 전체를 출력하기 위해, end_cursor의 위치를 \n 이나 EOF로 옮긴다.
        while scanner.src[end_cursor] != "\n" and scanner.src[end_cursor] != "\255":
            end_cursor += 1   
        line_src = scanner.src[start_cursor:end_cursor]

        super().__init__(msg +
                         f"\n{line_src}\n" +
                         f"{'-' * (scanner.line_cursor - 1)}^" +
                         f"\nline:{scanner.line+1}, pos:{scanner.line_cursor}")

class CharacterException(ScannerException):
    def __init__(self, scanner):
        super().__init__("해당 문자로 시작할 수 없습니다.", scanner)

class KeywordNotFoundException(ScannerException):
    def __init__(self, scanner):
        super().__init__("keyword table에서 해당 예약어를 찾을 수 없습니다.", scanner)

class FloatException(ScannerException):
    def __init__(self, scanner):
        super().__init__("올바르지 않은 실수 형식입니다.", scanner)

class OctalException(ScannerException):
    def __init__(self, scanner):
        super().__init__("올바르지 않은 8진수 형식입니다.", scanner)

class HexException(ScannerException):
    def __init__(self, scanner):
        super().__init__("올바르지 않은 16진수 형식입니다.", scanner)

class OperatorException(ScannerException):
    def __init__(self, operator, scanner):
        super().__init__(f"올바르지 않은 연산자: {operator}을 쓰려고 하셨습니까?.", scanner)

class ConstException(ScannerException):
    def __init__(self, type, scanner):
        type_str = "숫자" if type == 0 else "문자"
        super().__init__(f"올바르지 않은 {type_str} 상수입니다.", scanner)

class ParserException(Exception):
    def __init__(self, str="Parsing failed"):
        super().__init__(str)