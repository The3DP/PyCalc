#######################################
## The3DP                            ##
## Program progress: Updating...     ##                   
## Goal: Make a corrected            ##
## calculator using bare Python      ##
## based on corrections/improvements ##
## from 'Calc-v1.0'                  ##
#######################################

import math, readline, pickle, os, re
from sympy import symbols, sympify, sin, cos, tan, sqrt, log, factorial, diff, integrate, simplify, expand, solve, Eq
from sympy.plotting import plot
from sympy.physics.units import meter, centimeter, kilogram, gram, second, minute, hour, degree
from sympy.physics.units import convert_to
from sympy.core.sympify import SympifyError

# -----------------------------
# SMARTCALC v7.0 Ultimate
# -----------------------------
class Color:
    BLUE="\033[94m"; GREEN="\033[92m"; RED="\033[91m"; YELLOW="\033[93m"; CYAN="\033[96m"; RESET="\033[0m"; BOLD="\033[1m"

# Safe functions
SAFE_NAMES = {
    "pi": math.pi, "e": math.e, "tau": math.tau,
    "sin": sin, "cos": cos, "tan": tan, "sqrt": sqrt, "log": log, "ln": log, "fact": factorial,
    "diff": diff, "integrate": integrate, "simplify": simplify, "expand": expand, "solve": solve, "plot": plot,
    # Units
    "m": meter, "cm": centimeter, "kg": kilogram, "g": gram, "s": second, "min": minute, "h": hour, "deg": degree
}

# Persistent storage
SESSION_FILE = "smartcalc_session.pkl"
memory = {}
history = []
last_result = None
x = symbols('x')

def load_session():
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
    with open(SESSION_FILE, "wb") as f:
        pickle.dump({"memory": memory, "history": history, "last_result": last_result}, f)

def safe_eval(expr: str):
    global last_result
    if last_result is not None:
        expr = expr.replace("_", str(last_result))
    expr = re.sub(r"(\w+)\(([^()]*)d\)", r"\1((\2)*pi/180)", expr)

    # Assignment
    if "=" in expr:
        var, value_expr = map(str.strip, expr.split("=",1))
        value = sympify(value_expr, locals={**SAFE_NAMES, **memory})
        memory[var] = value
        last_result = value
        return f"{var} = {value}"

    # Solve multi-variable
    if expr.startswith("solve(") and expr.endswith(")"):
        inside = expr[6:-1]
        if inside.startswith("["):
            # list of equations
            eqs = sympify(inside, locals={**SAFE_NAMES, **memory})
            solutions = solve(eqs)
        else:
            eq = sympify(inside, locals={**SAFE_NAMES, **memory})
            solutions = solve(eq)
        last_result = solutions
        return solutions

    # Standard eval
    result = sympify(expr, locals={**SAFE_NAMES, **memory})
    last_result = result
    return result

def intro():
    print(f"{Color.BLUE}{Color.BOLD}Booting SmartCalc v7.0 Ultimate...{Color.RESET}")
    print("="*70)
    print("Supports: multi-variable solving, units, step-by-step solutions, plotting")
    print("Commands: help, vars, del var, history, clear, reset, exit")
    print("Use '_' for last result, e.g. '_ + 2'")
    print("-"*70)

def show_help():
    print(f"{Color.CYAN}Commands & Features:{Color.RESET}")
    print("Math functions:", ", ".join(sorted(SAFE_NAMES.keys())))
    print("Specials: _, sin(30d), solve([eq1, eq2], [x,y]), plot(expr), 5 cm + 2 m")
    print("Commands: help, vars, del var, history, clear, reset, exit\n")

def smart_calculator():
    global memory, last_result, history
    load_session()
    intro()
    while True:
        try:
            expr = input(f"{Color.YELLOW}>>> {Color.RESET}").strip()
            if not expr: continue
            history.append(expr)
            lower_expr = expr.lower()

            # Commands
            if lower_expr in {"exit","quit"}:
                save_session()
                print(f"{Color.CYAN}Goodbye! 👋{Color.RESET}")
                break
            elif lower_expr == "help":
                show_help(); continue
            elif lower_expr == "vars":
                print("Variables:", memory if memory else "No variables stored."); continue
            elif lower_expr.startswith("del "):
                var = expr.split(" ",1)[1].strip()
                if var in memory: del memory[var]; print(f"Deleted {var}"); continue
                print(f"{var} not found"); continue
            elif lower_expr == "clear":
                memory.clear(); print("Memory cleared"); continue
            elif lower_expr == "reset":
                memory.clear(); last_result=None; print("Reset complete"); continue
            elif lower_expr == "history":
                for i,e in enumerate(history,1): print(f"{i}: {e}"); continue

            # Evaluate
            result = safe_eval(expr)
            if str(result).startswith("Plot"): result.show()
            else: print(f"{Color.GREEN}Result: {result}{Color.RESET}\n")

        except Exception as e:
            print(f"{Color.RED}⚠️ Error: {e}{Color.RESET}\n")

if __name__ == "__main__":
    smart_calculator()
