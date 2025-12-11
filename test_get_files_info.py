from functions.get_files_info import get_files_info

def print_result(title: str, result: str) -> None:
    """Helper function to print test results clearly."""
    print(title)
    print(result)
    print("-" * 40) # Divider line for readability
    print()

if __name__ == "__main__":
    print("Running manual tests for 'get_files_info'...\n")

    # Test 1: Valid listing of the root directory
    print_result(
        '--- Test 1: List current directory (".") ---',
        get_files_info("calculator", ".")
    )

    # Test 2: Valid listing of a subdirectory
    print_result(
        "--- Test 2: List subdirectory ('pkg') ---",
        get_files_info("calculator", "pkg")
    )

    # Test 3: Security Check - Absolute path
    # Should fail because it is outside the working directory
    print_result(
        '--- Test 3: Attempt to list absolute path (\'/bin\') ---',
        get_files_info("calculator", "/bin")
    )

    # Test 4: Security Check - Path Traversal
    # Should fail because it tries to go up one level out of the sandbox
    print_result(
        '--- Test 4: Attempt Path Traversal ("../") ---',
        get_files_info("calculator", "../")
    )