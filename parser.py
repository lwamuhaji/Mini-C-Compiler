class Parser:
    def __init__(self):
        self.ch = None

    # E -> TE'
    def pE(self):
        self.pT(); self.pE_()
    
    # T	-> FT’
    def pT(self):
        self.pF(); self.pT_()
 
    # E' -> +TE' | -TE' | ε
    def pE_(self):
        if self.ch == '+':
            ...
        elif self.ch == '-':
            ...
        elif self.ch == '':
            ...
            
    def pT_(self):
        ...

    def pF(self):
        ...
    
    def pID(self):
        ...

# T’ -> *FT’ | /FT’ | ε
# F	-> (E) | ID
# ID -> a | b | c
# 