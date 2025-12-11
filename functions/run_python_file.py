import os
import subprocess
from typing import List, Optional

def run_python_file(working_directory: str, file_path: str, args: Optional[List[str]] = None) -> str:
    """
    Executes a Python script located within the working directory.

    Security:
        - Restricts execution to files inside 'working_directory'.
        - Enforces a 30-second timeout to prevent infinite loops.
        - Captures stdout and stderr to return feedback to the Agent.

    Args:
        working_directory (str): The root directory where execution is allowed.
        file_path (str): The relative path to the .py file.
        args (List[str], optional): A list of command-line arguments for the script.

    Returns:
        str: The combined output (STDOUT + STDERR) or an error message.
    """
    # Fix mutable default argument anti-pattern
    if args is None:
        args = []

    # Resolve absolute paths for security checks
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security Check 1: Prevent Path Traversal (e.g., accessing files outside the folder)
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'

    # Security Check 2: Ensure file exists
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    # Security Check 3: Ensure it is a Python file
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # Run the script using the system's 'python' interpreter.
        # cwd=working_directory ensures relative paths inside the script work correctly.
        result = subprocess.run(
            ["python", file_path] + args,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30  # Safety mechanism: Kill process if it takes too long
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        output_parts = []

        if stdout:
            output_parts.append(f"STDOUT:\n{stdout}")
        if stderr:
            output_parts.append(f"STDERR:\n{stderr}")
        
        # If the script crashed (non-zero exit code), report it
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return f"Error: The script '{file_path}' timed out after 30 seconds."
    except Exception as e:
        return f"Error executing Python file: {e}"