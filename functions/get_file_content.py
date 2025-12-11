import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Reads the content of a file within the permitted working directory.

    Security:
        - Prevents Path Traversal attacks by ensuring the resolved file path
          starts with the absolute working directory path.
        - Truncates content if it exceeds MAX_CHARS to prevent token limit issues.

    Args:
        working_directory (str): The base directory where file access is allowed.
        file_path (str): The relative path of the file to read.

    Returns:
        str: The content of the file, or an error message starting with 'Error:'.
    """
    # Resolve absolute paths to ensure accurate comparison
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security Check: Prevent accessing files outside the working directory
    # e.g., prevents input like "../../etc/passwd"
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'

    # Check if the file exists and is actually a file (not a directory)
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        # Open with UTF-8 encoding to support international characters
        # errors='replace' prevents crashing on non-text bytes
        with open(abs_file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(MAX_CHARS)
            
            # If the file is larger than the limit, append a truncation notice
            if os.path.getsize(abs_file_path) > MAX_CHARS:
                content += (
                    f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters...]'
                )
        return content

    except Exception as e:
        return f'Error reading file "{file_path}": {e}'