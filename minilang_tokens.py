# minilang_tokens.py
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
    
    DISPLAY = "DISPLAY"
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"

    STRING = "STRING"
    COMMA = "COMMA"

    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"

    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"

    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    
    NEWLINE = "NEWLINE"

# class used to tokenize MiniLang code to individual objects
class Token:
    # every token needs a value & type
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value
    # toString
    def __str__(self):
        return f"{self.token_type}: {self.value}"
