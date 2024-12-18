from scanner import Scanner
from tables import TokenID
from exceptions import ParserException

# Context Free Grammar
# E -> TE'
# T	-> FT’
# E' -> +TE' | -TE' | ε
# T’ -> *FT’ | /FT’ | ε 
# F	-> (E) | id | decimal

class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.tokens = []

    def parse(self):
        self.get_token_from_scanner()
        self.pE()
    
    def get_token_from_scanner(self):
        token = self.scanner.get_token()
        self.tokens.append(token)
        self.token = token

    # ----- Non-Terminal -----
    def pE(self): # E -> TE'
        self.pT(); self.pE_()

    def pT(self): # T	-> FT’
        self.pF(); self.pT_()

    def pE_(self): # E' -> +TE' | -TE' | ε
        if self.token == None:
            return
        elif self.token.get_id() == TokenID.PLUS:
            self.pPlus(); self.pT(); self.pE_()
        elif self.token.get_id() == TokenID.MINUS:
            self.pMinus(); self.pT(); self.pE_()
        else: pass

    def pT_(self): # T’ -> *FT’ | /FT’ | ε 
        if self.token == None:
            return
        elif self.token.get_id() == TokenID.MUL:
            self.pMultiple(); self.pF(); self.pT_()
        elif self.token.get_id() == TokenID.DIV:
            self.pDivide(); self.pF(); self.pT_()
        else: pass

    def pF(self): # F	-> (E) | id | decimal
        if self.token.get_id() == TokenID.OPEN_PARENTHESIS:
            self.pOpen(); self.pE(); self.pClose()
        elif self.token.get_id() == TokenID.ID:
            self.pid()
        else:
            self.pdecimal()
    
    # ----- Terminal -----
    def pid(self):
        if self.token.get_id() == TokenID.ID:
            self.get_token_from_scanner()
        else:
            raise ParserException()
    def pdecimal(self):
        if self.token.get_id() == TokenID.DEC:
            self.get_token_from_scanner()
        else:
            raise ParserException()
    def pPlus(self):
        if self.token.get_id() == TokenID.PLUS:
            self.get_token_from_scanner()
        else:
            raise ParserException()
    def pMinus(self):
        if self.token.get_id() == TokenID.MINUS:
            self.get_token_from_scanner()
        else:
            raise ParserException()        
    def pMultiple(self):
        if self.token.get_id() == TokenID.MUL:
            self.get_token_from_scanner()
        else:
            raise ParserException()        
    def pDivide(self):
        if self.token.get_id() == TokenID.DIV:
            self.get_token_from_scanner()
        else:
            raise ParserException()        
    def pOpen(self):
        if self.token.get_id() == TokenID.OPEN_PARENTHESIS:
            self.get_token_from_scanner()
        else:
            raise ParserException()        
    def pClose(self):
        if self.token.get_id() == TokenID.CLOSE_PARENTHESIS:
            self.get_token_from_scanner()
        else:
            raise ParserException()