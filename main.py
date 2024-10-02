import re
import time  # For implementing sleep

# Define keywords for the Telugu-based programming language
KEYWORDS = {
    "anuko": "SET",        # Variable Declaration
    "chupinchu": "PRINT",  # Print
    "sleep": "SLEEP",      # Sleep
    "+": "PLUS",           # Addition
    "-": "MINUS",          # Subtraction
    "*": "TIMES",          # Multiplication
    "/": "DIVIDE",         # Division
}

# Define token patterns
TOKEN_PATTERNS = [
    ("NUMBER", r"\d+"),
    ("STRING", r"\"[^\"]*\""),
    ("VAR", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("ASSIGN", r"="),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("TIMES", r"\*"),
    ("DIVIDE", r"/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("COMMENT", r"#.*"),   # Comments
    ("WS", r"\s+"),        # Whitespace
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

                # Skip comments and whitespace
                if token_type in ["COMMENT", "WS"]:
                    break

                # Replace keywords with corresponding tokens
                if token_type == "VAR" and lexeme in KEYWORDS:
                    token_type = KEYWORDS[lexeme]

                tokens.append((token_type, lexeme))
                break
        else:
            raise SyntaxError(f"Unknown character: {code[0]}")
    return tokens

# Define environment (variables) to hold state
variables = {}

# Helper function for evaluating expressions
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
        if token_type in ["PLUS", "MINUS", "TIMES", "DIVIDE"]:
            i += 1
            if token_type == "PLUS":
                result += parse_term()
            elif token_type == "MINUS":
                result -= parse_term()
            elif token_type == "TIMES":
                result *= parse_term()
            elif token_type == "DIVIDE":
                result //= parse_term()  # Integer division
        else:
            break

    return result

# Simple interpreter without conditions
def interpret(tokens):
    i = 0

    while i < len(tokens):
        token_type, token_value = tokens[i]

        if token_type == "SET":
            # Variable assignment
            i += 1
            var_name = tokens[i][1]
            i += 2  # Skip variable and assignment
            var_value = evaluate_expression(tokens, i)
            variables[var_name] = var_value

        elif token_type == "PRINT":
            i += 1
            var_value = evaluate_expression(tokens, i)
            print(var_value)

        i += 1  # Move to the next token

# Function to execute code from a .tll file
def execute_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
        tokens = lex(code)
        interpret(tokens)

# Execute the file
execute_file('example.tll')
