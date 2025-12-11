import sys
from typing import NoReturn

# Local imports
# Assumes that 'pkg' is a Python package (has __init__.py) in the same directory
from pkg.calculator import Calculator
from pkg.render import format_json_output

def main() -> None:
    """
    Main entry point for the Calculator Command Line Interface (CLI).
    
    It reads a mathematical expression from command line arguments,
    evaluates it using the Calculator class, and prints the result in JSON format.
    """
    calculator = Calculator()

    # Check if the user provided arguments.
    # sys.argv[0] is the script name, so we need at least one more argument.
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    # Join all arguments after the script name into a single string.
    # This allows users to type: python main.py 3 + 5 (without quotes)
    expression = " ".join(sys.argv[1:])

    try:
        # Attempt to calculate the result
        result = calculator.evaluate(expression)

        if result is not None:
            # Format the output as JSON for standard consumption by the Agent
            to_print = format_json_output(expression, result)
            print(to_print)
        else:
            # Handle cases where input was technically valid but empty
            print("Error: Expression is empty or contains only whitespace.")

    except Exception as e:
        # Catch any errors (like division by zero or invalid syntax)
        # and print them clearly so the Agent knows what went wrong.
        print(f"Error: {e}")


if __name__ == "__main__":
    main()