import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    """
    Writes content to a file, creating any necessary parent directories.
    
    Security:
        - Prevents Path Traversal attacks by validating that the target file
          remains within the 'working_directory'.
        - Overwrites existing files without warning (Agent behavior).

    Args:
        working_directory (str): The root permitted directory.
        file_path (str): The relative path where the file should be written.
        content (str): The text content to write.

    Returns:
        str: A success message with character count, or an error message.
    """
    # Resolve absolute paths to ensure accurate security checks
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security Check: Ensure we are not writing outside the sandbox
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory.'

    try:
        # Create parent directories if they don't exist
        # e.g., if writing to 'data/logs/error.txt', create 'data/logs/' first.
        dir_name = os.path.dirname(abs_file_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        # Write the content to the file using UTF-8 encoding
        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error writing file "{file_path}": {e}'