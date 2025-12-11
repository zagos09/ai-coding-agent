import os
from google.genai import types

# ==========================================
# Tool Definitions (Schemas)
# These schemas tell the AI model how to use the functions.
# ==========================================

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The directory to list files from, relative to the working "
                    "directory. If not provided, lists files in the working "
                    "directory itself."
                ),
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the file to read, relative to the working directory."
                ),
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file in the working directory with optional "
        "command-line arguments and returns its output."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Python file to run, relative to the working directory."
                ),
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description=(
                    "Optional list of arguments to pass to the Python file."
                ),
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file in the working directory with the provided content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
    ),
)

# Collection of all available tools to be passed to the model
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)


# ==========================================
# Function Implementation
# ==========================================

def get_files_info(working_directory: str, directory: str = ".") -> str:
    """
    Lists files and directories within a specified path, showing size and type.

    Security:
        - Prevents accessing directories outside the 'working_directory' (Path Traversal).

    Args:
        working_directory (str): The root permitted directory.
        directory (str): The sub-directory to list (relative to working_directory).

    Returns:
        str: A formatted list of files/folders or an error message.
    """
    try:
        # Construct full absolute paths
        target_path = os.path.join(working_directory, directory)
        abs_target = os.path.abspath(target_path)
        abs_working = os.path.abspath(working_directory)

        # Security Check: Ensure the target directory is inside the working directory
        if not abs_target.startswith(abs_working):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the path actually exists and is a directory
        if not os.path.isdir(abs_target):
            return f'Error: "{directory}" is not a directory'

        entries = os.listdir(abs_target)
        lines = []

        for entry in entries:
            entry_path = os.path.join(abs_target, entry)
            
            # Gather file stats
            is_dir = os.path.isdir(entry_path)
            size = os.path.getsize(entry_path)

            # Format the output line (e.g., "- main.py: file_size=1024 bytes, is_dir=False")
            lines.append(
                f"- {entry}: file_size={size} bytes, is_dir={str(is_dir)}"
            )

        return "\n".join(lines)

    except Exception as e:
        return f"Error listing files: {e}"