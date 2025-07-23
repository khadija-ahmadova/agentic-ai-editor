import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("API key not found")
        return 1

    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Prompt not provided\nUsage: python script.py <prompt>")
        return 1
    
    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )
    except Exception as e:
        print(f"API error: {e}")
        return 1
    
    for part in response.candidates[0].content.parts:
        if part.function_call:
            function_call_result = call_function(part.function_call, verbose=True)

            # Check if the function call succeeded and has a result
            if not hasattr(function_call_result.parts[0], "function_response") or \
            not hasattr(function_call_result.parts[0].function_response, "response"):
                raise RuntimeError("Function call failed: missing function_response.response")

            print(f"-> {function_call_result.parts[0].function_response.response}")
        elif part.text:
            print(part.text)


    if len(sys.argv) == 3:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def call_function(function_call_part, verbose=False):
    import functions.get_files_info as get_files_info
    import functions.get_file_content as get_file_content
    import functions.write_file as write_file
    import functions.run_python as run_python

    function_name = function_call_part.name
    args = dict(function_call_part.args)
    
    # Always inject working_directory manually
    args["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    # Dictionary mapping function names to actual functions
    function_map = {
        "get_files_info": get_files_info.get_files_info,
        "get_file_content": get_file_content.get_file_content,
        "write_file": write_file.write_file,
        "run_python_file": run_python.run_python_file
    }

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    try:
        result = function_map[function_name](**args)
    except Exception as e:
        result = f"Function raised an error: {str(e)}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )


if __name__ == "__main__":
    sys.exit(main())

