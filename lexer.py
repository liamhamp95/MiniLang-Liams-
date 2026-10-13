from token import Token, TokenType

# keeps track of source, position, and tokens
# source: MiniLang code
# position: MiniLang line

class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.tokens = []

    def current(self):
        if self.position >= len(self.source):
            return '\0'
        
        return self.source[self.position]
    
    def advance(self):
        self.position += 1

    def skip_whitespace(self):
        while self.current().isspace():
            self.advance()

    def read_number(self):
        start = self.position

        while self.current().isdigit():
            self.advance()
        
