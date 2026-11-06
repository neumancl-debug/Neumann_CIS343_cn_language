from error_handling import ErrorHandler
from token_type import TokenType
from expression_grammar import Binary, Literal, Grouping, Unary, Expression, Print

class ParseError(Exception):
    pass

# Parse class for handling expressions
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.error_handling = ErrorHandler()

    # Parses the list of tokens and returns the resulting expression tree
    def expression(self):
        return self.equality()
    
    # Parse equality expressions (== and !=)
    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    # Checks for a character type in the current token and advances if it matches
    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    # Checks if the current token is of the given type without advancing
    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type

    # Advances to the next token and returns the previous token
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    # Checks if the parser has reached the end of the token list
    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    # Returns the current token without advancing
    def peek(self):
        return self.tokens[self.current]

    # Returns the previous token
    def previous(self):
        return self.tokens[self.current - 1]

    # Parse comparison expressions (>, >=, <, <=)
    def comparison(self):
        expr = self.term()

        while self.match(
            TokenType.GREATER, 
            TokenType.GREATER_EQUAL, 
            TokenType.LESS, 
            TokenType.LESS_EQUAL):

            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    # Parse term expressions (+ and -)
    def term(self):
        expr = self.factor()

        while self.match(TokenType.PLUS, TokenType.MINUS):
        
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    # Parse factor expressions (* and /)
    def factor(self):
        expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.MODULO):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    # Parse unary expressions (! and -)
    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    # Parse primary expressions (literals and grouped expressions)
    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NULL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        
        if self.match(TokenType.STAR, TokenType.SLASH, TokenType.PLUS, TokenType.MODULO, TokenType.BANG_EQUAL, 
                      TokenType.EQUAL_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL, 
                      TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            raise self.error(operator, f"Missing left operand for {operator.lexeme}.")
            
        
        raise self.error(self.peek(), "Expect expression.")

    # Consumes a token of the expected type or raises an error if it doesn't match
    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    # Handles parsing errors by reporting them and returning a ParseError instance
    def error(self, token, message):
        ErrorHandler.error(token, message)
        return ParseError()

    # Synchronizes the parser after encountering an error to continue parsing subsequent statements.
    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in (
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ):
                return

            self.advance()

    # Parses the list of tokens and returns a list of statements (AST nodes).
    def parse(self):
        statements = []
        while not self.is_at_end():
            try:
                statements.append(self.statement())
            except ParseError:
                self.synchronize()
        return statements

    # Parses a single statement, which can be either a print statement or an expression statement.
    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()
        return self.expression_statement()

    # Parses a print statement, which consists of the 'print' keyword followed by an expression and a semicolon.
    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    # Parses an expression statement, which consists of an expression followed by a semicolon.
    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)