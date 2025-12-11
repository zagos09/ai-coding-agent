from functions.write_file import write_file

def print_result(description: str, result: str) -> None:
    """Helper to print test results with clear separation."""
    print(f"--- TEST: {description} ---")
    print(result)
    print("\n" + "="*40 + "\n")

def main():
    """
    Manual integration tests for 'write_file'.
    Verifies file creation, subdirectory handling, and security constraints.
    """

    # Test 1: Write a simple file in the root of the sandbox
    print_result(
        "Write to 'lorem.txt' (Root)",
        write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    )

    # Test 2: Write to a file inside a subdirectory (should create directories if needed)
    print_result(
        "Write to 'pkg/morelorem.txt' (Subdirectory)",
        write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    )

    # Test 3: Security Check - Attempt to write outside the sandbox
    # Expected: Error message
    print_result(
        "Security Check: Write outside allowed directory",
        write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    )

if __name__ == "__main__":
    main()