#######################################
## The3DP / d73928430@gmail.com      ##
##===================================##
## Program progress: Updating...     ##
## Goal: Make an accurate            ##
## calculator using bare Python.     ##
#######################################

def print_smartcalc_pseudocode():
    GREEN = "\033[92m"
    RESET = "\033[0m"

    pseudocode = f"""
{GREEN}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                        🟢 SMARTCALC v7.0 PSEUDOCODE 🟢                        ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                           BEGIN SMART_CALCULATOR                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  • IMPORT math module (and other modules like sympy, os, pickle, re)        ║
║                                                                              ║
║  • DEFINE allowed_names AS dictionary of math functions and constants       ║
║      (exclude any names starting with "__" for safety)                       ║
║                                                                              ║
║  • PRINT welcome message and usage instructions                              ║
║      e.g., "Type 'exit' to quit, use '_' for last result"                   ║
║                                                                              ║
║  • LOOP forever:                                                             ║
║      ▸ PROMPT user for an expression                                        ║
║                                                                              ║
║      ▸ IF expression is "exit" OR "quit":                                    ║
║            PRINT goodbye message                                             ║
║            BREAK loop                                                        ║
║                                                                              ║
║      ▸ TRY:                                                                  ║
║            IF expression contains "d)" (degree notation):                    ║
║                REPLACE "d)" with "*(pi/180))" to convert to radians         ║
║                                                                              ║
║            EVALUATE expression safely using allowed_names only               ║
║            STORE result in last_result                                       ║
║            PRINT result                                                      ║
║                                                                              ║
║      ▸ EXCEPT if an error occurs:                                           ║
║            PRINT error message with exception details                        ║
║                                                                              ║
║  • END LOOP                                                                  ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                               END PROGRAM                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝{RESET}
"""
    print(pseudocode)


# Call the function to display the green ASCII pseudocode
print_smartcalc_pseudocode()


import math

# -------------------------------
# SMART INTERACTIVE CALCULATOR
# -------------------------------
# This calculator:
# - Accepts typed expressions (like "2 + 3 * 5" or "sin(45)")
# - Supports mathematical functions (sin, cos, tan, sqrt, log, etc.)
# - Provides helpful feedback and handles errors gracefully
# -------------------------------

# A dictionary of safe math functions and constants
# This limits what the 'eval' function can access
allowed_names = {name: obj for name, obj in math.__dict__.items() if not name.startswith("__")}

def smart_calculator():
    print("booting . . .")
    print("Welcome to PyCalc!")
    print("[VERSION]: v1.0")
    print("Type 'exit' or 'quit' to stop.")
    print("Examples: 2 + 3 * 5, sin(45), sqrt(25), log(10, 2), (3 + 5)**2")
    print("-" * 50)

    while True:
        # Get user input
        expression = input("Enter expression: ").strip().lower()

        # Exit condition
        if expression in {"exit", "quit"}:
            print("Goodbye! 👋")
            break

        try:
            # Replace common degree-based trig shorthand with radians conversion
            # Example: sin(30d) → sin(math.radians(30))
            if expression.endswith("d)"):
                expression = expression.replace("d)", "*(pi/180))")

            # Evaluate safely using only math functions
            result = eval(expression, {"__builtins__": None}, allowed_names)
            print(f"Result: {result}\n")

        except Exception as e:
            print(f"⚠️ Error: {e}\n")
# Run the calculator
if __name__ == "__main__":
    smart_calculator()
