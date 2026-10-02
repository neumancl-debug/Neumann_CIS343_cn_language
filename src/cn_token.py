# Token class representing a token in the source code.
from token_type import TokenType

class Token:
    # Initializes a new Token instance
    def __init__(self, type:TokenType, lexeme:str, literal, line:int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        # Returns a string to represent the Token
        # --- Start AI Code ---
        quoted_lexeme = "'" + self.lexeme + "'"

        return (
            f"Token(type={str(self.type):<20}, "
            f"lexeme={quoted_lexeme:<20}, "
            f"literal={str(self.literal):<15}, "
            f"line={self.line})"
        )
        # --- End AI Code ---