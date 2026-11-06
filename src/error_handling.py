# Error handling utility for reporting errors in the source code.
from token_type import TokenType

class ErrorHandler:
    # Keeps track of whether an error has occurred
    has_error = False

    # Reports an error
    @staticmethod
    def error( token, message):
        if token.type == TokenType.EOF:
            ErrorHandler.report_error(token.line, " at end", message)
        else:
            ErrorHandler.report_error(token.line, f" at '{token.lexeme}'", message)

    # Reports an error with the line number and location
    @staticmethod
    def report_error(line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        ErrorHandler.has_error = True

# RuntimeError class for handling runtime errors during interpretation.
class RuntimeError(Exception):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token

    # Reports a runtime error with the line number and location.
    @staticmethod
    def runtime_error(error):
        print(f"{error}\n[line {error.token.line}]")
        ErrorHandler.has_error = True
    