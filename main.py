import re
import time  # For implementing sleep

# Define keywords for the Telugu-based programming language
KEYWORDS = {
    "anuko": "SET",        # Variable Declaration
    "aithe": "IF",         # If
    "lekunte": "ELIF",     # Elif
    "ledha": "ELSE",       # Else
    "chupinchu": "PRINT",  # Print
    "looplo": "LOOP",      # Loop
    "sleep": "SLEEP",      # Sleep
    "+": "PLUS",           # Addition
    "-": "MINUS",          # Subtraction
    "*": "TIMES",          # Multiplication
    "/": "DIVIDE",         # Division
    ">": "GT",             # Greater than
    "<": "LT",             # Less than
    ">=": "GTE",           # Greater than or equal
    "<=": "LTE",           # Less than or equal
    "==": "EQ",            # Equal to
    "!=": "NEQ",           # Not equal to
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
    ("GT", r">"),
    ("LT", r"<"),
    ("GTE", r">="),
    ("LTE", r"<="),
    ("EQ", r"=="),
    ("NEQ", r"!="),
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
        if token_type in ["PLUS", "MINUS", "TIMES", "DIVIDE", "GT", "LT", "GTE", "LTE", "EQ", "NEQ"]:
            i += 1
            if token_type == "PLUS":
                result += parse_term()
            elif token_type == "MINUS":
                result -= parse_term()
            elif token_type == "TIMES":
                result *= parse_term()
            elif token_type == "DIVIDE":
                result //= parse_term()  # Integer division
            elif token_type == "GT":
                result = result > parse_term()
            elif token_type == "LT":
                result = result < parse_term()
            elif token_type == "GTE":
                result = result >= parse_term()
            elif token_type == "LTE":
                result = result <= parse_term()
            elif token_type == "EQ":
                result = result == parse_term()
            elif token_type == "NEQ":
                result = result != parse_term()
        else:
            break

    return result

# Simple interpreter with proper IF, ELIF, ELSE handling
def interpret(tokens):
    i = 0
    skip_block = False  # To skip blocks after a condition is met

    while i < len(tokens):
        token_type, token_value = tokens[i]

        if token_type == "SET":
            # Variable assignment
            i += 1
            var_name = tokens[i][1]
            i += 2  # Skip variable and assignment
            var_value = evaluate_expression(tokens, i)
            variables[var_name] = var_value
            skip_block = False

        elif token_type == "PRINT":
            i += 1
            var_value = evaluate_expression(tokens, i)
            print(var_value)
            skip_block = False

        elif token_type == "IF":
            i += 1
            condition = evaluate_expression(tokens, i)
            if condition:
                skip_block = False
            else:
                skip_block = True
                # Skip the block until ELIF or ELSE
                while i < len(tokens) and tokens[i][0] not in ["ELIF", "ELSE", "ENDIF"]:
                    i += 1

        elif token_type == "ELIF":
            if skip_block:
                i += 1
                condition = evaluate_expression(tokens, i)
                if condition:
                    skip_block = False
                else:
                    # Skip the block if ELIF is also false
                    while i < len(tokens) and tokens[i][0] not in ["ELSE", "ENDIF"]:
                        i += 1
            else:
                # Skip the block if previous IF/ELIF was true
                while i < len(tokens) and tokens[i][0] != "ENDIF":
                    i += 1

        elif token_type == "ELSE":
            if skip_block:
                skip_block = False  # Execute the ELSE block
            else:
                # Skip ELSE block if IF or ELIF was true
                while i < len(tokens) and tokens[i][0] != "ENDIF":
                    i += 1

        i += 1

# Function to execute code from a .tll file
def execute_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
        tokens = lex(code)
        interpret(tokens)

execute_file('example.tll')
