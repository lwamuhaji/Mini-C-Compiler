from scanner import Scanner
from tables import TokenID
from exceptions import ParserException
from enum import Enum

# Rule1 : E  -> TE'
# Rule2 : E' -> +TE'
# Rule3 : E' -> -TE'
# Rule4 : E' -> ε
# Rule5 : T  -> FT'
# Rule6 : T' -> *FT'
# Rule7 : T' -> /FT'
# Rule8 : T' -> ε
# Rule9 : F  -> (E)
# Rule10: F  -> id

class Rule(Enum):
    Rule1  = 1
    Rule2  = 2
    Rule3  = 3
    Rule4  = 4
    Rule5  = 5
    Rule6  = 6
    Rule7  = 7
    Rule8  = 8
    Rule9  = 9
    Rule10 = 10

    def __str__(self):
        if self.name == "Rule1":
            return "E  -> TE'"
        if self.name == "Rule2":
            return "E' -> +TE'"
        if self.name == "Rule3":
            return "E' -> -TE'"
        if self.name == "Rule4":
            return "E' -> ε"
        if self.name == "Rule5":
            return "T  -> FT'"
        if self.name == "Rule6":
            return "T' -> *FT'"
        if self.name == "Rule7":
            return "T' -> /FT'"
        if self.name == "Rule8":
            return "T' -> ε"
        if self.name == "Rule9":
            return "F  -> (E)"
        if self.name == "Rule10":
            return "F  -> id"

parsing_table = {
    "E": {
        TokenID.DEC: Rule.Rule1,
        TokenID.OPEN_PARENTHESIS: Rule.Rule1,
    },
    "E'": {
        TokenID.PLUS: Rule.Rule2,
        TokenID.MINUS: Rule.Rule3,
        TokenID.CLOSE_PARENTHESIS: Rule.Rule4,
        None: Rule.Rule4,
    },
    "T": {
        TokenID.DEC: Rule.Rule5,
        TokenID.OPEN_PARENTHESIS: Rule.Rule5,
    },
    "T'": {
        TokenID.PLUS: Rule.Rule8,
        TokenID.MINUS: Rule.Rule8,
        TokenID.CLOSE_PARENTHESIS: Rule.Rule8,
        None: Rule.Rule8,
        TokenID.MUL: Rule.Rule6,
        TokenID.DIV: Rule.Rule7,
    },
    "F": {
        TokenID.DEC: Rule.Rule10,
        TokenID.OPEN_PARENTHESIS: Rule.Rule9,
    },
}

class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.token = None
        self.stack = []
    
    def get_token_from_scanner(self):
        token = self.scanner.get_token()
        self.token = token

    def apply_rule(self, rule: Rule):
        self.stack.pop()
        if rule == Rule.Rule1:
            self.stack.append("E'")
            self.stack.append("T")
        elif rule == Rule.Rule2:
            self.stack.append("E'")
            self.stack.append("T")
            self.stack.append(TokenID.PLUS)
        elif rule == Rule.Rule3:
            self.stack.append("E'")
            self.stack.append("T")
            self.stack.append(TokenID.MINUS)
        elif rule == Rule.Rule4:
            pass
        elif rule == Rule.Rule5:
            self.stack.append("T'")
            self.stack.append("F")
        elif rule == Rule.Rule6:
            self.stack.append("T'")
            self.stack.append("F")
            self.stack.append(TokenID.MUL)
        elif rule == Rule.Rule7:
            self.stack.append("T'")
            self.stack.append("F")
            self.stack.append(TokenID.DIV)
        elif rule == Rule.Rule8:
            pass
        elif rule == Rule.Rule9:
            self.stack.append(TokenID.CLOSE_PARENTHESIS)
            self.stack.append("E")
            self.stack.append(TokenID.OPEN_PARENTHESIS)
        elif rule == Rule.Rule10:
            self.stack.append(TokenID.DEC)

    def parse(self):
        self.stack = ['$', 'E']
        tokens = []
        while True:
            token = self.scanner.get_token()
            if token:
                tokens.append(token.get_id())
            else:
                tokens.append(None)
                break

        print(self.stack)

        while True:
            top = self.stack[-1]
            token_id = tokens[0]

            if top == '$' and token_id == None: # 구문분석 완료
                break
            elif top == token_id: # 일치
                print("매칭!")
                self.stack.pop()
                tokens.pop(0)
                print('[ ', end='')
                for t in self.stack:
                    print(t, end=' ')
                print(']   [ ', end='')
                for t in tokens:
                    print(t, end=' ')
                print(']')
            else: # 불일치
                rule = parsing_table[top][token_id]
                print("선택된 룰:", rule)
                self.apply_rule(rule)
                print('[ ', end='')
                for t in self.stack:
                    print(t, end=' ')
                print(']  [ ', end='')
                for t in tokens:
                    print(t, end=' ')
                print(']')

        print("구문분석 완료")

if __name__ == "__main__":
    sentence = "4 * (20 - 10)"
    print("구문분석 대상:", sentence, end='\n\n')
    scanner = Scanner(sentence)
    parser = Parser(scanner)
    parser.parse()