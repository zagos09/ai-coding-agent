import json
from typing import Union

def format_json_output(expression: str, result: float, indent: int = 2) -> str:
    """
    Formats the calculation result into a structured JSON string.
    
    This function prepares the output to be easily readable by both humans and 
    other software components (like an AI agent consuming the tool output).

    Args:
        expression (str): The original mathematical expression (e.g., "10 + 5").
        result (float): The numeric result of the calculation.
        indent (int, optional): The indentation level for the JSON string. Defaults to 2.

    Returns:
        str: A JSON-formatted string containing the expression and the result.
    """
    
    # Variable to hold the final value we want to display
    result_to_dump: Union[int, float]

    # Check if the float is actually a whole number (e.g., 5.0).
    # If yes, convert to int (5) for cleaner output.
    if isinstance(result, float) and result.is_integer():
        result_to_dump = int(result)
    else:
        result_to_dump = result

    output_data = {
        "expression": expression,
        "result": result_to_dump,
    }
    
    return json.dumps(output_data, indent=indent)