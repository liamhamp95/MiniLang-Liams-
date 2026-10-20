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

    # method to read a number
    def read_number(self):
        start = self.position

        while self.current().isdigit():
            self.advance()
            
        number = self.source[start:self.position]
        
        return Token(TokenType.NUMBER, number)
    
    # method to read an identifier
    def read_identifier(self):
        start = self.position
        
        while self.current().asalnum() or self.current() == '_':
            self.advance()
        
        world = self.source[start:self.position]
        
        keywords = {
            "make": TokenType.LET,
            "equal":  TokenType.ASSIGN,
            "show": TokenType.DISPLAY,
            "plus": TokenType.PLUS,
        }
        
        token_type = keywords.get(word, TokenType.IDENTIFIER)
        
        return Token(token_type,word)