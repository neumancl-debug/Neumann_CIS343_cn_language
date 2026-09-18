import sys

class cn:
    @staticmethod
    def main():
        args = sys.argv[1:]

        if len(args)> 1:
            print("Usage: cn [script]")
            sys.exit(64)

        elif len(args) == 1:
            run_file(args[0])

        else:
            run_prompt()


def run_file(path):
    with open(path, 'r') as file:
        source = file.read()
    run(source)


def run_prompt():
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        run(line)

            
def run(source):
    print(source)
    print("Scanner not implemented")

def Scanner(source):
    pass

if __name__ == "__main__":
    cn.main()