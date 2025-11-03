#######################################
## The3DP                            ##
## Program progress: Updating...     ##                   
## Goal: Make a corrected            ##
## calculator using bare Python      ##
## based on corrections/improvements ##
## from 'Calc-v1.0'                  ##
#######################################

'''
╔═════════════════════════════════════════════════════════════════════════════╗
║                        PyCalc-v2.0 Pseudocode Manual                        ║
╠═════════════════════════════════════════════════════════════════════════════╣

-- Constants and Setup ----------------------------------------------------------
Color class:
    BLUE, GREEN, RED, YELLOW, CYAN, RESET, BOLD

SAFE_NAMES dictionary:
    Constants: pi, e, tau
    Math functions: sin, cos, tan, sqrt, log, ln, fact,
                    diff, integrate, simplify, expand, solve, Eq, plot
    Units: m, cm, kg, g, s, min, h, deg

SESSION_FILE = "smartcalc_session.pkl"
memory = {}        # Stores user-defined variables
history = []       # Stores user input commands
last_result = None # Holds most recent result

-- Load Session -----------------------------------------------------------------
FUNCTION load_session():
    IF SESSION_FILE exists:
        TRY:
            OPEN and UNPICKLE session file
            RESTORE memory, history, and last_result
        EXCEPT:
            IGNORE any errors

-- Save Session -----------------------------------------------------------------
FUNCTION save_session():
    OPEN SESSION_FILE for writing (binary)
    PICKLE {memory, history, last_result}

-- Safe Evaluation --------------------------------------------------------------
FUNCTION safe_eval(expr):
    REPLACE "_" with last_result (if exists)
    CONVERT degree notation (e.g., sin(30d) → sin(30*pi/180))

    IF expression contains "=" (and not "=="):
        SPLIT into variable and value expression
        EVALUATE right-hand side safely
        STORE in memory[var]
        SET last_result = value
        RETURN "var = value"

    ELSE IF expression starts with "solve(" and ends with ")":
        PARSE inside of solve()
        CALL SymPy.solve() on expression
        UPDATE last_result
        RETURN solutions

    ELSE:
        SAFELY evaluate expression using sympy.sympify()
        UPDATE last_result
        RETURN result

-- Intro ------------------------------------------------------------------------
FUNCTION intro():
    PRINT boot header, version, supported features, and command list

-- Help -------------------------------------------------------------------------
FUNCTION show_help():
    PRINT all available math functions, units, and calculator commands

-- Main Calculator Loop ---------------------------------------------------------
FUNCTION smart_calculator():
    CALL load_session()
    CALL intro()

    LOOP FOREVER:
        PROMPT user with ">>> "
        READ input string
        IF input is empty, CONTINUE loop
        ADD input to history

        MATCH commands:
            "exit" or "quit" → CALL save_session(), PRINT goodbye, BREAK
            "help"           → CALL show_help()
            "vars"           → PRINT stored variables
            "del <var>"      → DELETE variable from memory
            "clear"          → CLEAR all memory
            "reset"          → CLEAR memory and reset last_result
            "history"        → PRINT all stored commands
        OTHERWISE:
            CALL safe_eval(input)
            IF result is a plot object:
                SHOW plot
            ELSE:
                PRINT formatted result

-- Program Entry Point ----------------------------------------------------------
IF __name__ == "__main__":
    CALL smart_calculator()

╚═════════════════════════════════════════════════════════════════════════════╝
'''

import math, readline, pickle, os, re
from sympy import (
    symbols, sympify, sin, cos, tan, sqrt, log, factorial,
    diff, integrate, simplify, expand, solve, Eq
)
from sympy.plotting import plot
from sympy.physics.units import meter, centimeter, kilogram, gram, second, minute, hour, degree
from sympy.core.sympify import SympifyError

# -----------------------------
# PyCalc v2.0 
# -----------------------------
class Color:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

# Safe functions and constants
SAFE_NAMES = {
    "pi": math.pi, "e": math.e, "tau": math.tau,
    "sin": sin, "cos": cos, "tan": tan,
    "sqrt": sqrt, "log": log, "ln": log,
    "fact": factorial,
    "diff": diff, "integrate": integrate,
    "simplify": simplify, "expand": expand,
    "solve": solve, "Eq": Eq, "plot": plot,
    # Units
    "m": meter, "cm": centimeter, "kg": kilogram, "g": gram,
    "s": second, "min": minute, "h": hour, "deg": degree
}

SESSION_FILE = "smartcalc_session.pkl"
memory = {}
history = []
last_result = None

def load_session():
    """Load persistent session data."""
    global memory, history, last_result
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "rb") as f:
                data = pickle.load(f)
                memory = data.get("memory", {})
                history = data.get("history", [])
                last_result = data.get("last_result", None)
        except Exception:
            pass

def save_session():
    """Save persistent session data."""
    with open(SESSION_FILE, "wb") as f:
        pickle.dump({"memory": memory, "history": history, "last_result": last_result}, f)

def safe_eval(expr: str):
    """Safely evaluate mathematical expressions."""
    global last_result

    if last_result is not None:
        expr = expr.replace("_", str(last_result))

    # Convert degree notation (e.g., sin(30d))
    expr = re.sub(r"(\w+)\(([^()]*)d\)", r"\1((\2)*pi/180)", expr)

    # Handle variable assignment
    if "=" in expr and not expr.strip().startswith("=="):
        var, value_expr = map(str.strip, expr.split("=", 1))
        try:
            value = sympify(value_expr, locals={**SAFE_NAMES, **memory})
        except SympifyError as e:
            raise ValueError(f"Invalid expression: {value_expr}") from e
        memory[var] = value
        last_result = value
        return f"{var} = {value}"

    # Handle solve() syntax
    if expr.startswith("solve(") and expr.endswith(")"):
        try:
            inside = sympify(expr[6:-1], locals={**SAFE_NAMES, **memory})
            solutions = solve(inside)
            last_result = solutions
            return solutions
        except Exception as e:
            raise ValueError(f"Error solving expression: {e}")

    # Evaluate normally
    try:
        result = sympify(expr, locals={**SAFE_NAMES, **memory})
    except SympifyError as e:
        raise ValueError(f"Invalid syntax: {expr}") from e

    last_result = result
    return result

def intro():
    print(f"{Color.BLUE}{Color.BOLD}Booting SmartCalc v2.0 ...{Color.RESET}")
    print("=" * 70)
    print("Supports: symbolic math, solving, units, and plotting")
    print("Commands: help, vars, del var, history, clear, reset, exit")
    print("Use '_' for last result, e.g. '_ + 2'")
    print("-" * 70)

def show_help():
    print(f"{Color.CYAN}Commands & Features:{Color.RESET}")
    print("Math functions:", ", ".join(sorted(SAFE_NAMES.keys())))
    print("Specials: _, sin(30d), solve([eq1, eq2], [x,y]), plot(expr), 5*cm + 2*m")
    print("Commands: help, vars, del var, history, clear, reset, exit\n")

def smart_calculator():
    load_session()
    intro()

    while True:
        try:
            expr = input(f"{Color.YELLOW}>>> {Color.RESET}").strip()
            if not expr:
                continue

            lower_expr = expr.lower()
            history.append(expr)

            # --- Commands ---
            if lower_expr in {"exit", "quit"}:
                save_session()
                print(f"{Color.CYAN}Goodbye! 👋{Color.RESET}")
                break
            elif lower_expr == "help":
                show_help()
                continue
            elif lower_expr == "vars":
                print("Variables:", memory if memory else "No variables stored.")
                continue
            elif lower_expr.startswith("del "):
                var = expr.split(" ", 1)[1].strip()
                if var in memory:
                    del memory[var]
                    print(f"Deleted {var}")
                else:
                    print(f"{var} not found")
                continue
            elif lower_expr == "clear":
                memory.clear()
                print("Memory cleared")
                continue
            elif lower_expr == "reset":
                memory.clear()
                globals()["last_result"] = None
                print("Reset complete")
                continue
            elif lower_expr == "history":
                for i, e in enumerate(history, 1):
                    print(f"{i}: {e}")
                continue

            # --- Evaluate expression ---
            result = safe_eval(expr)
            if hasattr(result, "show"):  # Handle plot objects
                result.show()
            else:
                print(f"{Color.GREEN}Result: {result}{Color.RESET}\n")

        except Exception as e:
            print(f"{Color.RED}⚠️ Error: {e}{Color.RESET}\n")

if __name__ == "__main__":
    smart_calculator()
