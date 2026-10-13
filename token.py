# token.py
# Liam Hampshire & Liam Shum

# defined token types
class TokenType:
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"

    LET = "LET"

    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    POWER = "POWER"

    ASSIGN = "ASSIGN"

    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    SEMICOLON = "SEMICOLON"

    EOF = "EOF"

# class used to tokenize MiniLang code to individual objects
class Token:
    # every token needs a value & type
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value
    # toString
    def __str__(self):
        return f"{self.token_type}: {self.value}"
