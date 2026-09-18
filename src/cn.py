import sys

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

# Starts REPL and takes input until EOF or CTRL+C
def run_repl():
    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            break
        run_source(line)

# Wll eventually run the scanner     
def run_source(source):
    print(source)
    print("Scanner Not Implemented")

def scanner(source):
    #Scanner function will be implemeted in the future
    pass

if __name__ == "__main__":
    main()