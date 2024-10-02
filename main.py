import re
import time  # For implementing sleep

# Define keywords for the Telugu-based programming language
KEYWORDS = {
    "anuko": "SET",        # Variable Declaration
    "aithe": "IF",        # If
    "lekunte": "ELIF",    #Elif
    "ledha": "ELSE",    # Else
    "chupinchu": "PRINT",    # Print
    "looplo": "LOOP",     # Loop
    "sleep": "SLEEP",     # Sleep
    "+": "PLUS",         # Addition
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
    ("STRING", r"\"[^\"]*\""),  # Strings in double quotes
    ("LIST", r"\[.*?\]"),       # Lists in square brackets
    ("TUPLE", r"\(.*?\)"),      # Tuples in parentheses
    ("DICT", r"\{.*?\}"),       # Dictionaries in curly braces
    ("VAR", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("ASSIGN", r"="),
    ("PLUS", r"\+"),     # Escaped + symbol
    ("MINUS", r"-"),     # No need to escape -
    ("TIMES", r"\*"),    # Escaped * symbol
    ("DIVIDE", r"/"),    # No need to escape /
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
            print(var_value)

        elif token_type == "IF":
            i += 1
            condition = evaluate_expression(tokens, i)
            if condition:
                i += 1  # Move to the next token inside the if block
                while i < len(tokens) and tokens[i][0] not in ["ELSE", "ENDIF"]:
                    token_type, token_value = tokens[i]
                    if token_type == "PRINT":
                        i += 1
                        var_value = evaluate_expression(tokens, i)
                        print(var_value)
                    else:
                        i += 1
                # Skip the ELSE block if condition was true
                while i < len(tokens) and tokens[i][0] != "ENDIF":
                    i += 1
            else:
                # Skip to ELSE or ENDIF if condition is false
                while i < len(tokens) and tokens[i][0] not in ["ELSE", "ENDIF"]:
                    i += 1
                if i < len(tokens) and tokens[i][0] == "ELSE":
                    i += 1  # Move past ELSE
                    while i < len(tokens) and tokens[i][0] != "ENDIF":
                        token_type, token_value = tokens[i]
                        if token_type == "PRINT":
                            i += 1
                            var_value = evaluate_expression(tokens, i)
                            print(var_value)
                        else:
                            i += 1

        i += 1

# Function to execute code from a .tll file
def execute_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
        tokens = lex(code)
        interpret(tokens)

execute_file('example.tll')
