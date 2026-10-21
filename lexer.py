from minilang_tokens import Token, TokenType

# keeps track of source, position, and tokens
# source: MiniLang code
# position: index of the current character in source
# line: current line number (used in error messages)
# trace: when True, prints every token as it is created

class Lexer:
    def __init__(self, source, trace=False):
        self.source = source
        self.position = 0
        self.line = 1
        self.tokens = []
        self.trace = trace

    def current(self):
        if self.position >= len(self.source):
            return '\0'

        return self.source[self.position]

    # looks one character ahead without moving (needed for <=, ==, &&, //)
    def peek(self):
        if self.position + 1 >= len(self.source):
            return '\0'

        return self.source[self.position + 1]

    def advance(self):
        if self.current() == '\n':
            self.line += 1
        self.position += 1

    # raises an error that includes the line number
    def error(self, message):
        raise SyntaxError(f"Error (line {self.line}): {message}")

    # adds a token to the list (and prints it in trace mode)
    def add_token(self, token_type, value):
        token = Token(token_type, value)
        token.line = self.line
        self.tokens.append(token)

        if self.trace:
            if value is None:
                print(f"[TOKEN] {token_type}")
            else:
                print(f"[TOKEN] {token_type} {value}")

    # method to read a number
    # DFA states:
    #   START --digit--> INT
    #   INT   --digit--> INT
    #   INT   --'.'--->  DOT
    #   DOT   --digit--> FRAC
    #   FRAC  --digit--> FRAC
    # accepting states: INT, FRAC   (DOT is not accepting, so "5." is an error)
    def read_number(self):
        start = self.position
        state = "INT"
        self.advance()  # first digit already checked by tokenize()

        while True:
            character = self.current()

            if state == "INT" and character.isdigit():
                state = "INT"
            elif state == "INT" and character == '.':
                state = "DOT"
            elif state == "DOT" and character.isdigit():
                state = "FRAC"
            elif state == "FRAC" and character.isdigit():
                state = "FRAC"
            else:
                break

            self.advance()

        number = self.source[start:self.position]

        if state == "DOT":
            self.error(f"Malformed number '{number}'.")

        # a letter right after a number (like 3abc) is not valid
        if self.current().isalpha() or self.current() == '_':
            self.error(f"Invalid number '{number}{self.current()}'.")

        if state == "FRAC":
            self.add_token(TokenType.NUMBER, float(number))
        else:
            self.add_token(TokenType.NUMBER, int(number))

    # method to read an identifier
    # DFA states:
    #   START --letter or _--> IDENT
    #   IDENT --letter, digit, or _--> IDENT
    # accepting state: IDENT, then check if the word is a keyword
    def read_identifier(self):
        start = self.position

        while self.current().isalnum() or self.current() == '_':
            self.advance()

        word = self.source[start:self.position]

        keywords = {
            "let": TokenType.LET,
            "display": TokenType.DISPLAY,
            "if": TokenType.IF,
            "then": TokenType.THEN,
            "else": TokenType.ELSE,
        }

        token_type = keywords.get(word, TokenType.IDENTIFIER)

        self.add_token(token_type, word)

    # method to read a string in quotes
    # accepts straight quotes "..." and the curly quotes used in the handout
    def read_string(self):
        opening = self.current()

        if opening == '“':
            closing = '”'
        else:
            closing = '"'

        self.advance()  # skip opening quote
        start = self.position

        while self.current() != closing:
            if self.current() in ('\0', '\n'):
                self.error("Unterminated string, missing closing quote.")
            self.advance()

        text = self.source[start:self.position]
        self.advance()  # skip closing quote

        self.add_token(TokenType.STRING, text)

    # method to read an operator that might be two characters long
    # DFA: read the first character, then look at the next one
    #   '<' -> LESS,     '<' then '=' -> LESS_EQUAL
    #   '>' -> GREATER,  '>' then '=' -> GREATER_EQUAL
    #   '=' -> ASSIGN,   '=' then '=' -> EQUAL
    #   '!' -> NOT,      '!' then '=' -> NOT_EQUAL
    #   '&' then '&' -> AND   (a single '&' is an error)
    #   '|' then '|' -> OR    (a single '|' is an error)
    def read_operator(self):
        first = self.current()
        second = self.peek()

        one_char = {
            '<': TokenType.LESS,
            '>': TokenType.GREATER,
            '=': TokenType.ASSIGN,
            '!': TokenType.NOT,
        }

        two_char = {
            '<=': TokenType.LESS_EQUAL,
            '>=': TokenType.GREATER_EQUAL,
            '==': TokenType.EQUAL,
            '!=': TokenType.NOT_EQUAL,
            '&&': TokenType.AND,
            '||': TokenType.OR,
        }

        pair = first + second

        if pair in two_char:
            self.advance()
            self.advance()
            self.add_token(two_char[pair], pair)

        elif first in one_char:
            self.advance()
            self.add_token(one_char[first], first)

        else:
            self.error(f"Invalid character '{first}'. Did you mean '{first * 2}'?")

    # main loop that reads source and chooses which method to call.
    def tokenize(self):
        # operators and punctuation that are always one character
        single_char = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '–': TokenType.MINUS,  # en dash, from copying the handout
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,
            '^': TokenType.POWER,
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
        }

        # keeps scanning until end
        while self.current() != '\0':
            character = self.current()

            # skips spaces, tabs, and newlines
            # (newlines are whitespace because if/then/else can span lines)
            if character in ' \t\r\n':
                self.advance()

            # skips a // comment until the end of the line
            elif character == '/' and self.peek() == '/':
                while self.current() not in ('\n', '\0'):
                    self.advance()

            # creates token if found number
            elif character.isdigit():
                self.read_number()

            # create token if found letter or underscore
            elif character.isalpha() or character == '_':
                self.read_identifier()

            # creates token if found a string
            elif character in ('"', '“'):
                self.read_string()

            # operators that might be two characters (<=, ==, &&, ...)
            elif character in '<>=!&|':
                self.read_operator()

            # one-character operators and punctuation
            elif character in single_char:
                self.add_token(single_char[character], character)
                self.advance()

            # anything else is an invalid character
            else:
                self.error(f"Invalid character '{character}'.")

        # adds end of file token to token list
        self.add_token(TokenType.EOF, None)
        return self.tokens
