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
        self.token = None

    def parse(self):
        self.get_token_from_scanner()
        if not self.token:
            return False
        self.pS()
        return True
    
    def get_token_from_scanner(self):
        token = self.scanner.get_token()
        self.tokens.append(token)
        self.token = token

    # ----- Non-Terminal -----
    def pS(self): # S -> id=E | E
        if self.token.get_id() == TokenID.ID:
            self.pid(); self.pequal(); self.pE()
        else:
            self.pE()

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
    def pequal(self):
        print(self.token.get_id())
        if self.token.get_id() == TokenID.ASSIGN:
            self.get_token_from_scanner()
        else:
            raise ParserException("=가 아님")
    def pid(self):
        print(self.token)
        if self.token.get_id() == TokenID.ID:
            self.get_token_from_scanner()
        else:
            raise ParserException("id가 아님")
    def pdecimal(self):
        print(self.token)
        if self.token.get_id() == TokenID.DEC:
            self.get_token_from_scanner()
        else:
            raise ParserException("10 진수가 아님")
    def pPlus(self):
        print(self.token.get_id())
        if self.token.get_id() == TokenID.PLUS:
            self.get_token_from_scanner()
        else:
            raise ParserException("+가 아님")
    def pMinus(self):
        print(self.token.get_id())
        if self.token.get_id() == TokenID.MINUS:
            self.get_token_from_scanner()
        else:
            raise ParserException("-가 아님")
    def pMultiple(self):
        print(self.token.get_id())
        if self.token.get_id() == TokenID.MUL:
            self.get_token_from_scanner()
        else:
            raise ParserException("*가 아님") 
    def pDivide(self):
        print(self.token.get_id())
        if self.token.get_id() == TokenID.DIV:
            self.get_token_from_scanner()
        else:
            raise ParserException("/가 아님")        
    def pOpen(self):
        print(self.token.get_id())
        if self.token.get_id() == TokenID.OPEN_PARENTHESIS:
            self.get_token_from_scanner()
        else:
            raise ParserException("(가 아님") 
    def pClose(self):
        print(self.token.get_id())
        if self.token.get_id() == TokenID.CLOSE_PARENTHESIS:
            self.get_token_from_scanner()
        else:
            raise ParserException(")가 아님")