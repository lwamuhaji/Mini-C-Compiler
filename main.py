import sys
from scanner import Scanner

if __name__ == "__main__":
    # default src
    src = """
    int A, B, Sum;
    float _x1, _y1, _zoom;
    char _ch1;
    if (A>B) Sum = A+B
    else Sum = A+10;
    while (A ==B) {
    _zoom = (Sum + _x1)/10;
    _ch1 = ‘123’;
    }
    """

    if len(sys.argv) == 1:
        print("입력된 파일 경로가 없으므로 default src를 사용합니다.")
    else:
        with open(sys.argv[1], encoding='utf-8') as f:
            src = f.read()

    scanner = Scanner(src)
    try:
        while token := scanner.get_token():
            print(token)
    except Exception as e:
        print("[에러발생]", e)