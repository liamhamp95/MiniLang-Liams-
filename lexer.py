from minilang_tokens import Token, TokenType

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
        
        while self.current().isalnum() or self.current() == '_':
            self.advance()
        
        word = self.source[start:self.position]
        
        keywords = {
            "make": TokenType.LET,
            "equal":  TokenType.ASSIGN,
            "show": TokenType.DISPLAY,
            "plus": TokenType.PLUS,
        }
        
        token_type = keywords.get(word, TokenType.IDENTIFIER)
        
        return Token(token_type,word)
    
    # main loop that reads source and chooses which method to call.
    def tokenize(self):
        # keeps scanning until end
        while self.current() != '\0':
            character = self.current()
            
            # skips spaces or tabs
            if character in ' \t\r':
                self.advance()
            
            # creates newline token
            elif character == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n'))
                self.advance()
            
            # creates token if found number
            elif character.isdigit():
                self.tokens.append(self.read_number())
                
            # create token if found letter or underscore    
            elif character.isalpha() or character == '_':
                self.tokens.append(self.read_identifier())
            
            # anything else produces error currently    
            else:
                raise SyntaxError(
                    f"Unexpected character '{character}' "
                    f"at position {self.position}"
                )
        
        # adds end of file token to token list
        self.tokens.append(Token(TokenType.EOF, None))
        return self.tokens