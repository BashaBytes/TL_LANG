import tkinter as tk
from tkinter import messagebox
import re
import time

# Updated Telugu programming language keywords and tokens
KEYWORDS = {
    "anuko": "SET",
    "chupinchu": "PRINT",
    "anki": "FLOAT",
    "sleep": "SLEEP",
    "looplo": "LOOP",
    "+": "PLUS",
    "-": "MINUS",
    "*": "TIMES",
    "/": "DIVIDE",
    ">": "GT",
    "<": "LT",
    ">=": "GTE",
    "<=": "LTE",
    "==": "EQ",
    "!=": "NEQ",
}

TOKEN_PATTERNS = [
    ("FLOAT", r"\d+\.\d+"),
    ("NUMBER", r"\d+"),
    ("STRING", r"\"[^\"]*\""),
    ("LIST", r"\[.*?\]"),
    ("TUPLE", r"\(.*?\)"),
    ("DICT", r"\{.*?\}"),
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
    ("COMMENT", r"#.*"),
    ("WS", r"\s+"),
]

variables = {}

def lex(code):
    tokens = []
    while code:
        for token_type, pattern in TOKEN_PATTERNS:
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                lexeme = match.group(0)
                code = code[len(lexeme):]

                if token_type == "COMMENT":
                    break
                if token_type == "WS":
                    break
                if token_type == "VAR" and lexeme in KEYWORDS:
                    token_type = KEYWORDS[lexeme]
                tokens.append((token_type, lexeme))
                break
        else:
            raise SyntaxError(f"Unknown character: {code[0]}")
    return tokens

def evaluate_expression(tokens, i):
    def parse_term():
        nonlocal i
        token_type, token_value = tokens[i]
        i += 1
        if token_type == "NUMBER":
            return int(token_value)
        elif token_type == "FLOAT":
            return float(token_value)
        elif token_type == "STRING":
            return token_value.strip('"')
    
           
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
            result /= parse_term()
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

def interpret(tokens):
    i = 0
    while i < len(tokens):
        token_type, token_value = tokens[i]
        if token_type == "SET":
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
            output_display.insert(tk.END, f"{var_value}\n")
        elif token_type == "INPUT":
            i += 1
            prompt = tokens[i][1]
            result = input(prompt.strip('"') + ": ")
            variables[prompt] = result
        elif token_type == "SLEEP":
            i += 1
            sleep_time = evaluate_expression(tokens, i)
            time.sleep(sleep_time)
        elif token_type == "LOOP":
            i += 1
            iterations = evaluate_expression(tokens, i)
            loop_start = i
            for _ in range(iterations):
                interpret(tokens[loop_start:])
        i += 1

def execute_telugu_code(code):
    try:
        tokens = lex(code)
        interpret(tokens)
        return "Execution Successful"
    except Exception as e:
        return str(e)

# Tkinter GUI setup
root = tk.Tk()
root.title("TL_LANG")

# Create a text area for input
code_input_label = tk.Label(root, text="Enter your Code Here:")
code_input_label.pack()

code_input = tk.Text(root, height=10, width=50)
code_input.pack()

# Create an output area for result display
output_display = tk.Text(root, height=10, width=50)
output_display.pack()

def run_code():
    code = code_input.get("1.0", tk.END).strip()
    output_display.delete("1.0", tk.END)  # Clear previous output
    result = execute_telugu_code(code)
    output_display.insert(tk.END, f"{result}\n")

# Create a run button
run_button = tk.Button(root, text="Run Code", command=run_code)
run_button.pack()

# Run the Tkinter loop
root.geometry("500x500")
root.resizable(0,0)
root.mainloop()
