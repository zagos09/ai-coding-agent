from typing import List, Optional, Union

class Calculator:
    """
    A simple infix calculator that evaluates mathematical expressions.
    It supports basic arithmetic operators (+, -, *, /) and respects operator precedence.
    """

    def __init__(self):
        # Mapping of string symbols to actual Python lambda functions
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        
        # Define operator precedence (higher number = higher priority)
        # Multiplication/Division happen before Addition/Subtraction
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression: str) -> Optional[float]:
        """
        Evaluates a string mathematical expression.
        
        Args:
            expression (str): The mathematical expression (e.g., "3 + 4 * 2").
                              NOTE: Tokens must be separated by spaces.

        Returns:
            Optional[float]: The result of the calculation, or None if input is empty.
        """
        if not expression or expression.isspace():
            return None
        
        # Split the string by spaces to get tokens (numbers and operators)
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens: List[str]) -> float:
        """
        Core logic to evaluate infix notation using two stacks: values and operators.
        """
        values: List[float] = []      # Stack to store numbers
        operators: List[str] = []     # Stack to store operators (+, -, *, /)

        for token in tokens:
            if token in self.operators:
                # If token is an operator, handle precedence.
                # While there is an operator at the top of the stack with 
                # greater or equal precedence, apply it first.
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                
                # Push the current operator onto the stack
                operators.append(token)
            else:
                # If token is not an operator, assume it's a number
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid token encountered: {token}")

        # After processing all tokens, apply remaining operators in the stack
        while operators:
            self._apply_operator(operators, values)

        # The final result should be the only item left in the values stack
        if len(values) != 1:
            raise ValueError("Invalid expression format")

        return values[0]

    def _apply_operator(self, operators: List[str], values: List[float]) -> None:
        """
        Helper function to pop one operator and two operands, perform the operation,
        and push the result back to the values stack.
        """
        if not operators:
            return

        operator = operators.pop()

        # We need at least two numbers to perform a binary operation
        if len(values) < 2:
            raise ValueError(f"Not enough operands for operator {operator}")

        # Pop the last two values (LIFO order)
        b = values.pop()
        a = values.pop()
        
        # Calculate and append result
        result = self.operators[operator](a, b)
        values.append(result)