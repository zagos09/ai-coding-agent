from functions.run_python_file import run_python_file
from typing import List, Optional

def run_test(description: str, file_path: str, args: Optional[List[str]] = None):
    """
    Helper function to print the test case description and the result clearly.
    """
    print(f"--- TEST: {description} ---")
    print(f"Input: file='{file_path}', args={args}")
    
    # Call the tool
    result = run_python_file("calculator", file_path, args)
    
    print("Result:")
    print(result)
    print("\n" + "="*50 + "\n")

def main():
    """
    Manual integration tests for 'run_python_file'.
    """

    # 1. Test executing main.py without arguments
    # Expected: Should print usage instructions (Calculator App Usage...)
    run_test("Run main.py (no args)", "main.py")

    # 2. Test executing main.py WITH arguments
    # Expected: Should calculate 3 + 5 and return JSON {"result": 8}
    run_test("Run main.py with args", "main.py", ["3 + 5"])

    # 3. Test executing the unit tests
    # Expected: Should run unittest and show "OK" or failures
    run_test("Run unit tests", "tests.py")

    # 4. Security Test: Path Traversal
    # Expected: Error (Cannot execute ... outside permitted directory)
    run_test("Security: Path Traversal", "../main.py")

    # 5. Error Test: File not found
    # Expected: Error (File not found)
    run_test("Error: Non-existent file", "nonexistent.py")

    # 6. Error Test: Not a Python file
    # Expected: Error (is not a Python file)
    run_test("Error: Invalid file type", "lorem.txt")

if __name__ == "__main__":
    main()