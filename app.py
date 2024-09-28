from flask import Flask, render_template, request
import re
import time
import os

app = Flask(__name__)

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define keywords for the Telugu-based programming language
KEYWORDS = {
    "petu": "SET",        # Variable Declaration
    "aithe": "IF",        # If
    "lekunte": "ELSE",    # Else
    "cheppu": "PRINT",    # Print
    "looplo": "LOOP",     # Loop
    "tuples": "TUPLE",    # Tuple
    "lists": "LIST",      # List
    "dict": "DICT",       # Dictionary
    "sleep": "SLEEP",     # Sleep
    "+": "PLUS",          # Addition
    "-": "MINUS",         # Subtraction
    "*": "TIMES",         # Multiplication
    "/": "DIVIDE",        # Division
    ">": "GT",            # Greater than
    "<": "LT",            # Less than
    ">=": "GTE",          # Greater than or equal
    "<=": "LTE",          # Less than or equal
    "==": "EQ",           # Equal to
    "!=": "NEQ",          # Not equal to
}

# Define token patterns for variables, numbers, strings, lists, tuples, and symbols
TOKEN_PATTERNS = [
    ("NUMBER", r"\d+"),
    ("STRING", r'"([^"\\]*(\\.[^"\\]*)*)"?'),  # Handle escaped characters in strings
    ("LIST", r"\[.*?\]"),       # Lists in square brackets
    ("TUPLE", r"\(.*?\)"),      # Tuples in parentheses
    ("DICT", r"\{.*?\}"),       # Dictionaries in curly braces
    ("VAR", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("ASSIGN", r"="),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("TIMES", r"\*"),
    ("DIVIDE", r"/"),
    ("GT", r">"),
    ("LT", r"<"),
    ("GTE", r">="),
    ("LTE", r"<="),
    ("EQ", r"=="),
    ("NEQ", r"!="),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("COMMENT", r"#.*"),   # Comments
    ("WS", r"\s+"),  # Whitespace
]

# Lexer function
def lex(code):
    tokens = []
    while code:
        for token_type, pattern in TOKEN_PATTERNS:
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                lexeme = match.group(0)
                code = code[len(lexeme):]

                # Skip comments
                if token_type == "COMMENT":
                    break

                # Skip whitespace
                if token_type == "WS":
                    break

                # Replace keywords with corresponding tokens
                if token_type == "VAR" and lexeme in KEYWORDS:
                    token_type = KEYWORDS[lexeme]

                tokens.append((token_type, lexeme))
                break
        else:
            raise SyntaxError(f"Unknown character: {code[0]}")
    return tokens

# Define the environment (variables) to hold the state
variables = {}

# Helper function for arithmetic, string, and comparison operations
def evaluate_expression(tokens, i):
    def parse_term():
        nonlocal i
        token_type, token_value = tokens[i]
        i += 1

        if token_type == "NUMBER":
            return int(token_value)
        elif token_type == "STRING":
            return token_value.strip('"')
        elif token_type == "LIST":
            return eval(token_value)  # Convert list string to Python list
        elif token_type == "TUPLE":
            return eval(token_value)  # Convert tuple string to Python tuple
        elif token_type == "DICT":
            return eval(token_value)  # Convert dictionary string to Python dict
        elif token_type == "VAR":
            if token_value in variables:
                return variables[token_value]
            else:
                raise NameError(f"Undefined variable: {token_value}")

    result = parse_term()

    while i < len(tokens):
        token_type, token_value = tokens[i]

        if token_type == "PLUS":
            i += 1
            result += parse_term()
        elif token_type == "MINUS":
            i += 1
            result -= parse_term()
        elif token_type == "TIMES":
            i += 1
            result *= parse_term()
        elif token_type == "DIVIDE":
            i += 1
            result //= parse_term()  # Integer division
        elif token_type == "GT":
            i += 1
            result = result > parse_term()
        elif token_type == "LT":
            i += 1
            result = result < parse_term()
        elif token_type == "GTE":
            i += 1
            result = result >= parse_term()
        elif token_type == "LTE":
            i += 1
            result = result <= parse_term()
        elif token_type == "EQ":
            i += 1
            result = result == parse_term()
        elif token_type == "NEQ":
            i += 1
            result = result != parse_term()
        else:
            break

    return result

# Simple interpreter with IF, ELSE, LOOP support, sleep, and variable types (lists, dicts, etc.)
def interpret(tokens):
    i = 0
    output = []
    while i < len(tokens):
        token_type, token_value = tokens[i]

        if token_type == "SET":
            # Variable assignment
            i += 1
            var_name = tokens[i][1]
            i += 1
            if tokens[i][0] == "ASSIGN":
                i += 1
                var_value = evaluate_expression(tokens, i)
                variables[var_name] = var_value

        elif token_type == "PRINT":
            i += 1
            var_value = evaluate_expression(tokens, i)
            output.append(str(var_value))  # Append to output instead of printing

        elif token_type == "SLEEP":
            i += 1
            sleep_time = evaluate_expression(tokens, i)
            time.sleep(sleep_time)  # Sleep for a specified time

        elif token_type == "IF":
            i += 1
            condition = evaluate_expression(tokens, i)
            if condition:
                output += interpret(tokens[i:])  # Execute true block and collect output
            else:
                # Skip ahead to ELSE if present
                while i < len(tokens) and tokens[i][0] != "ELSE":
                    i += 1
                if i < len(tokens) and tokens[i][0] == "ELSE":
                    i += 1
                    output += interpret(tokens[i:])  # Execute false block and collect output

        elif token_type == "LOOP":
            i += 1
            iterations = evaluate_expression(tokens, i)
            loop_start = i
            for _ in range(iterations):
                output += interpret(tokens[loop_start:])

        i += 1

    return output

# Function to execute the Telugu code
def execute_telugu_code(code):
    global variables
    variables = {}  # Reset variables before execution
    try:
        tokens = lex(code)
        output = interpret(tokens)
        return "\n".join(output)  # Return joined output for web display
    except Exception as e:
        return str(e)

# Function to execute code from a .tll file
def execute_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
        return execute_telugu_code(code)

# The route to display the web page
@app.route('/', methods=['GET', 'POST'])
def home():
    result = ''
    if request.method == 'POST':
        if 'code' in request.form:
            code = request.form['code']
            result = execute_telugu_code(code)
        elif 'file' in request.files:
            file = request.files['file']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            result = execute_file(file_path)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
