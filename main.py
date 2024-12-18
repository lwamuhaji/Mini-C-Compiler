import sys
from scanner import Scanner
from parser import Parser

if __name__ == "__main__":
    # default src
    src = """
    A ++ B - C
    """

    if len(sys.argv) == 1:
        print("입력된 파일 경로가 없으므로 default src를 사용합니다.\n")
    else:
        # 주어진 인자 경로로 소스 파일을 불러 읽어들인다.
        with open(sys.argv[1], encoding='utf-8') as f:
            src = f.read()
    
    scanner = Scanner(src) # src로 Scanner 인스턴스 생성
    parser = Parser(scanner)
    parser.parse()