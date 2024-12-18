from scanner import Scanner
from mc_token import TokenID

# E -> TE'
# T	-> FT’
# E' -> +TE' | -TE' | ε
# T’ -> *FT’ | /FT’ | ε 
# F	-> (E) | ID
# ID -> A | B | C

class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner

    def parse(self):
        self.token = self.scanner.get_token()
        self.pE()
        print("구문분석 완료")

    # E -> TE'
    def pE(self):
        self.pT(); self.pE_()
    
    # T	-> FT’
    def pT(self):
        self.pF(); self.pT_()
 
    # E' -> +TE' | -TE' | ε
    def pE_(self):
        if self.token == None:
            return
        elif self.token.get_id() == TokenID.PLUS:
            self.pPlus(); self.pT(); self.pE_()
        elif self.token.get_id() == TokenID.MINUS:
            self.pMinus(); self.pT(); self.pE_()
        else:
            ...

    # T’ -> *FT’ | /FT’ | ε 
    def pT_(self):
        if self.token == None:
            return
        elif self.token.get_id() == TokenID.MUL:
            self.pMultiple(); self.pF(); self.pT_()
        elif self.token.get_id() == TokenID.DIV:
            self.pDivide(); self.pF(); self.pT_()
        else:
            ...

    # F	-> (E) | ID
    def pF(self):
        if self.token.get_id() == TokenID.OPEN_PARENTHESIS:
            self.pOpen(); self.pE(); self.pClose()
        else:
            self.pID()
    
    # ID -> A | B | C
    def pID(self):
        if self.token.get_id() == TokenID.ID:
            if self.token.get_char() == 'A':
                self.pA()
            elif self.token.get_char() == 'B':
                self.pB()
            elif self.token.get_char() == 'C':
                self.pC()
        else:
            raise Exception()

    # ----- Terminal -----
    def pPlus(self):
        if self.token.get_id() == TokenID.PLUS:
            print(self.token)
            self.token = self.scanner.get_token()
        else:
            raise Exception()
    def pMinus(self):
        if self.token.get_id() == TokenID.MINUS:
            print(self.token)
            self.token = self.scanner.get_token()
        else:
            raise Exception()        
    def pMultiple(self):
        if self.token.get_id() == TokenID.MUL:
            print(self.token)
            self.token = self.scanner.get_token()
        else:
            raise Exception()        
    def pDivide(self):
        if self.token.get_id() == TokenID.DIV:
            print(self.token)
            self.token = self.scanner.get_token()
        else:
            raise Exception()        
    def pOpen(self):
        if self.token.get_id() == TokenID.OPEN_PARENTHESIS:
            print(self.token)
            self.token = self.scanner.get_token()
        else:
            raise Exception()        
    def pClose(self):
        if self.token.get_id() == TokenID.CLOSE_PARENTHESIS:
            print(self.token)
            self.token = self.scanner.get_token()
        else:
            raise Exception()        
    def pA(self):
        if self.token.get_id() == TokenID.ID and self.token.get_char() == 'A':
            print(self.token)
            self.token = self.scanner.get_token()
        else:
            raise Exception()        
    def pB(self):
        if self.token.get_id() == TokenID.ID and self.token.get_char() == 'B':
            print(self.token)
            self.token = self.scanner.get_token()
        else:
            raise Exception()        
    def pC(self):
        if self.token.get_id() == TokenID.ID and self.token.get_char() == 'C':
            print(self.token)
            self.token = self.scanner.get_token()
        else:
            raise Exception()