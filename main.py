import sys
from pathlib import Path
from lexer import Lexer
 
# runs a MiniLang program from a text file
 
def main():
    # gets the file name and checks for --trace
    args = sys.argv[1:]
    trace = "--trace" in args
    files = [arg for arg in args if arg != "--trace"]
    if not files:
        project_folder = Path(__file__).resolve().parent
        files = [str(project_folder / "examples" / "sample.txt")]
 
    if len(files) != 1:
        print("Usage: python main.py <file.txt> [--trace]")
        sys.exit(1)
 
    filename = files[0]
 
    # reads the MiniLang source code from the file
    try:
        with open(filename, encoding="utf-8") as file:
            source = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
 
    # breaks the source code into tokens
    try:
        tokens = Lexer(source, trace=trace).tokenize()
    except SyntaxError as error:
        print(error)
        sys.exit(1)
 
    # prints the tokens like the handout example: LET, IDENTIFIER(x), NUMBER(5)
    # (in trace mode the lexer already printed them)
    if not trace:
        for token in tokens:
            if token.token_type in ("IDENTIFIER", "NUMBER", "STRING"):
                print(f"{token.token_type}({token.value})")
            else:
                print(token.token_type)
 
    # next steps:
    #   program = Parser(tokens, trace=trace).parse_program()
    #   Interpreter(trace=trace).execute(program)
 
 
if __name__ == "__main__":
    main()
