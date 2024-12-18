from scanner import Scanner
from parser import Parser
from exceptions import ParserException, ScannerException
from lib import *

print("Mini-C Interpreter")

while True:
    sentence = input('>>> ')

    if sentence == 'exit':
        break
    
    scanner = Scanner(sentence)
    parser = Parser(scanner)
    try:
        parser.parse() # 구문분석
        tokens = infix_to_postfix(parser.tokens[:-1]) # 토큰을 역폴란드표기법으로 변환
        result = eval_post(tokens)
        print(result)
    except ParserException as e:
        print('[Parsing Error]', e, end="\n\n")
    except ScannerException as e:
        print('[Scanner Error]', e, end="\n\n")
    