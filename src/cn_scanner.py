# Scanner class for the CN programming language, responsible for converting source code into tokens
from error_handling import ErrorHandler
from cn_token import Token
from token_type import TokenType

class Scanner:
    # Intialize the scanner with the source code and set up for tokenization
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

        # Define the reserved keywords for the CN language
        self.keywords = { 
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "elseif": TokenType.ELSEIF,
            "null": TokenType.NULL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
            "const": TokenType.CONST,
            "break": TokenType.BREAK
        }

    # Scan the source code and return the tokens
    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    # Check if the current position is at the end of the source code
    def is_at_end(self):
        return self.current >= len(self.source)

    # Return the current character and advance the position
    def advance(self):
            character = self.source[self.current]
            self.current += 1
            return character 

    # Scan a single token
    def scan_token(self):
        c = self.advance()

        # Determine the type of token based on the current character
        if c =="(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c ==")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c =="{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c =="}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c ==",":
            self.add_token(TokenType.COMMA)
        elif c ==".": 
            self.add_token(TokenType.DOT)
        elif c =="-":
            self.add_token(TokenType.MINUS)
        elif c =="+":
            self.add_token(TokenType.PLUS)
        elif c ==";":
            self.add_token(TokenType.SEMICOLON)
        elif c =="*":
            self.add_token(TokenType.STAR)
        elif c =="/":
            self.add_token(TokenType.SLASH)
        elif c=="%":
            self.add_token(TokenType.MODULO)
        
        # Handle operators with two characters
        elif c =="!":
            if self.match("="):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif c =="=":
            if self.match("="):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif c== "<":
            if self.match("="):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif c== ">":
            if self.match("="):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)

        # Handle comments and whitespace
        elif c == "#":
            if self.match("*"):
                self.block_comment()
            else:
                while self.lookahead() != "\n" and not self.is_at_end():
                    self.advance()
        elif c in (" ", "\r", "\t"):
            pass
        elif c == "\n":
            self.line += 1
        
        # Handle string literals
        elif c == '"':
            self.string()
        else:
            if self.is_digit(c):
                self.number()
            elif self.is_alpha(c):
                self.identifier()
            else:
                ErrorHandler.report_error(self.line, f" at character: {c}", "Unexpected character")

    # Add a token to the list of tokens
    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    # Check if the current character matches the expected character, advances the scanner
    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    # Returns the current character without advancing the scanner
    def lookahead(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    # Scans a string literal, checks for double quotes at both the beginning and the end
    def string(self):
        while self.lookahead() != '"' and not self.is_at_end():
            if self.lookahead() == "\n":
                self.line += 1
            self.advance()

        # Raise an error if a string is unterminated
        if self.is_at_end():
            ErrorHandler.report_error(self.line, "", "Unterminated string.")
            return
        
        # The string terminates and a string token is added
        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    # Defines number literals
    def is_digit(self, c):
        return '0' <= c <= '9'

    # Defines alphabetic characters and underscores as valid identifier characters
    def is_alpha(self, c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == "_"

    # Scans a number literal
    def number(self):
        while self.is_digit(self.lookahead()):
            self.advance()

        # Looks for digits after a decimal point
        if self.lookahead() == "." and self.is_digit(self.lookahead_next()):
            self.advance()

            while self.is_digit(self.lookahead()):
                self.advance()

        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    # Scans an identifier
    def identifier(self):
        while self.is_alpha(self.lookahead()) or self.is_digit(self.lookahead()):
            self.advance()

        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    # Returns the next character without advancing the scanner
    def lookahead_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    # Scans a block comment, handling nested comments and reporting unterminated comments
    def block_comment(self):
        depth_counter = 1
        while not self.is_at_end():
            if self.lookahead() == "#" and self.lookahead_next() == "*":
                self.advance()
                self.advance()
                depth_counter +=1
            elif self.lookahead() == "*" and self.lookahead_next() == "#":
                self.advance()
                self.advance()
                depth_counter -= 1
                
                if depth_counter == 0:
                    return
            else:
                if self.lookahead() == "\n":
                    self.line += 1
                self.advance()
        ErrorHandler.report_error(self.line, "", "Unterminated block comment.")
