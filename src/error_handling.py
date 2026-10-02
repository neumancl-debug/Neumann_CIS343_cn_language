# Error handling utility for reporting errors in the source code.

class ErrorHandler:
    # Keeps track of whether an error has occurred
    has_error = False

    # Reports an error
    @staticmethod
    def error(line, message):
        ErrorHandler.report_error(line, "", message)

    # Reports an error with the line number and location
    @staticmethod
    def report_error(line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        ErrorHandler.has_error = True