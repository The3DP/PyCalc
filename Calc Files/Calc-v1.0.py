#######################################
## The3DP                            ##
## Expected Finish Date:             ##
## 11/1/2025                         ##
## Goal: Make an accurate            ##
## calculator using bare Python.     ##
#######################################
#PSEUDOCODE:

###========================================================================================##
##BEGIN SMART_CALCULATOR                                                                   ##                                                                 
##                                                                                         ##
##    IMPORT math module                                                                   ##
##                                                                                         ##
##    DEFINE allowed_names AS dictionary of math functions and constants                   ##
##        (exclude anything that starts with "__")                                         ##
##                                                                                         ##
##    PRINT welcome messages and usage examples                                            ##
##                                                                                         ##
##    LOOP forever:                                                                        ##
##        PROMPT user for an expression                                                    ##
##                                                                                         ##
##        IF expression is "exit" OR "quit":                                               ##
##            PRINT goodbye message                                                        ##
##            BREAK the loop                                                               ##
##                                                                                         ##
##        TRY:                                                                             ##
##            IF expression ends with "d)":                                                ##
##                REPLACE "d)" with "*(pi/180))" to convert degrees to radians             ##
##                                                                                         ##
##            EVALUATE expression using only allowed_names (safe eval)                     ##
##            PRINT the result                                                             ##
##                                                                                         ##
##        EXCEPT if an error occurs:                                                       ##
##            PRINT an error message with the exception details                            ##
##                                                                                         ##
##    END LOOP                                                                             ##
##                                                                                         ##
##END PROGRAM                                                                              ##
###========================================================================================##

#=CODE:

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
    print("🧮 Smart Interactive Calculator")
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
