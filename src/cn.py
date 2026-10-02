# Entry point for the CN programming language interpreter, integrates the scanner and error handling
import sys
from error_handling import ErrorHandler
from cn_scanner import Scanner

def main():
    # Receive the arguements from the command line
    args = sys.argv[1:]

    # Exit if more than one argument is given
    if len(args)> 1:
        print("Usage: cn [script]")
        sys.exit(64)

    # Run the file if exactly one argument is given
    elif len(args) == 1:
        run_file(args[0])

    # Run REPL if no arguments are given
    else:
        run_repl()


# Run the given file
def run_file(path):
    with open(path, 'r') as file:
        source = file.read()
    
    run_source(source)

    return 65 if ErrorHandler.has_error else 0

# Starts REPL and takes input until EOF or CTRL+C
def run_repl():
    while True:
        try:
            line = input("> ")
        except EOFError:
            print("\nEOF received. Exiting REPL.")
            break
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt. Exiting REPL.")
            break
        run_source(line)

# Runs the source code through the scanner and prints the resulting tokens
def run_source(source):
    ErrorHandler.has_error = False

    for token in Scanner(source).scan_tokens():
       print(token)

if __name__ == "__main__":
    main()