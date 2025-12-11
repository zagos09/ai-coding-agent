from functions.get_file_content import get_file_content

def main():
    """
    Manual integration test for the 'get_file_content' tool.
    
    Verifies that:
    1. Standard file reading works.
    2. Reading from subdirectories works.
    3. Security restrictions (Path Traversal) function correctly.
    """
    
    print("--- Test 1: Read 'main.py' from 'calculator' directory ---")
    # Should print the content of calculator/main.py containing "def main():"
    print(get_file_content("calculator", "main.py"))
    print("\n" + "="*30 + "\n")

    print("--- Test 2: Read 'pkg/calculator.py' (subdirectory) ---")
    # Should print the content containing "def _apply_operator..."
    print(get_file_content("calculator", "pkg/calculator.py"))
    print("\n" + "="*30 + "\n")

    print("--- Test 3: Security Check (Path Traversal) ---")
    # Attempt to read a file outside the working directory (pyproject.toml)
    # Expected Output: An Error message starting with "Error:"
    print(get_file_content("calculator", "../pyproject.toml"))

if __name__ == "__main__":
    main()