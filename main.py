import os
import argparse
import sys
from typing import Dict, Any, Optional

# Third-party imports
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Local imports
from prompts import system_prompt
from functions.get_files_info import available_functions, get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

# Load environment variables from .env file
load_dotenv()

# Configuration
# The directory where the agent is allowed to work (sandbox)
WORKING_DIRECTORY = "./calculator"
MODEL_NAME = "gemini-2.0-flash-exp" # or "gemini-2.0-flash" depending on availability

# Map string names to actual Python functions
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call_part: types.Part, verbose: bool = False) -> types.Content:
    """
    Executes a specific tool (function) requested by the model.

    Args:
        function_call_part: The part of the response containing the function call details.
        verbose (bool): Whether to print detailed logs.

    Returns:
        types.Content: The output of the tool wrapped in a format the model understands.
    """
    function_name = function_call_part.name
    original_args = function_call_part.args
    
    # Create a copy of args to inject the secure working directory
    new_args = dict(original_args)
    new_args["working_directory"] = WORKING_DIRECTORY
    
    target_function = function_map.get(function_name)

    if target_function is None:
        # Handle case where model hallucinates a non-existent function
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Logging
    if verbose:
        print(f"Calling function: {function_name}({original_args})")
    else:
        print(f" - Calling function: {function_name}...")

    # Execute the actual Python function
    try:
        function_result = target_function(**new_args)
    except Exception as e:
        function_result = f"Error executing tool: {e}"

    # Return the result back to the model
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


def main():
    """
    Main Agent Loop.
    
    Flow:
    1. User inputs a prompt.
    2. Model thinks and decides if it needs to use a tool.
    3. If tool needed -> Script executes tool -> Returns result to Model -> Loop back to 2.
    4. If no tool needed -> Model gives final answer -> Exit.
    """
    
    # 1. API Key Validation
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found. Please create a .env file with your key.")

    # 2. Argument Parsing
    parser = argparse.ArgumentParser(description="AI Agent with Python Execution Capabilities")
    parser.add_argument("user_prompt", type=str, help="The instruction for the agent")
    parser.add_argument("--verbose", action="store_true", help="Enable detailed logging")
    args = parser.parse_args()

    # 3. Client Initialization
    client = genai.Client(api_key=api_key)
    
    # Initialize conversation history with the user's prompt
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    max_iterations = 20
    response = None

    print(f"🤖 Agent started. Goal: '{args.user_prompt}'")

    # 4. Main Reasoning Loop
    for i in range(max_iterations):
        try:
            # Step 1: Send history to the model and get a response
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions],
                    temperature=0.0, # Keep it deterministic for code generation
                ),
            )

            if not response.candidates:
                print("Error: No candidates returned from model.")
                break

            # Add the model's response (thoughts/function calls) to history
            for candidate in response.candidates:
                messages.append(candidate.content)

            function_call_results = []

            # Step 2: Check if the model wants to call functions
            if response.function_calls:
                # Execute each function call
                for call in response.function_calls:
                    result = call_function(call, verbose=args.verbose)
                    
                    # Validate the structure of the result
                    if (
                        not hasattr(result, "parts")
                        or not result.parts
                        or not hasattr(result.parts[0], "function_response")
                    ):
                        raise RuntimeError("Function call returned invalid format.")

                    part = result.parts[0]
                    function_call_results.append(part)

                    if args.verbose:
                        print(f"   -> Tool Output: {part.function_response.response}")

                # Step 3: Append tool results to history so the model can see them
                if function_call_results:
                    tool_message = types.Content(
                        role="user", # In GenAI SDK, tool outputs often come as user role
                        parts=function_call_results,
                    )
                    messages.append(tool_message)

                # Continue the loop to let the model process the tool results
                continue  

            # Step 4: No function calls? We have the final answer.
            if response.text:
                print("\n✅ Final Response:")
                print(response.text)
                break
            else:
                print("Model returned no text and no function calls. Stopping.")
                break

        except Exception as e:
            print(f"\n❌ Error during agent loop: {e}")
            break

    # 5. Usage Statistics
    if response and response.usage_metadata:
        prompt_tokens = response.usage_metadata.prompt_token_count
        resp_tokens = response.usage_metadata.candidates_token_count
        
        if args.verbose:
            print("\n--- Usage Stats ---")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {resp_tokens}")


if __name__ == "__main__":
    main()