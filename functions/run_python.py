import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not full_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        completed_process = subprocess.run(
            ["python3", file_path, *args],
            capture_output=True,
            cwd=working_directory,
            timeout=30,
            text=True
        )
        output = ""
        
        if completed_process.stdout:
            output += f"STDOUT: {completed_process.stdout}"
        if completed_process.stderr:
            output += f"STDERR: {completed_process.stderr}"
        if completed_process.returncode != 0:
            output += f"Process exited with code {completed_process.returncode}"

        if not output.strip():
            return "No output produced."
        
        return output
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory, optionally with command-line arguments. Returns standard output and error.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of arguments to pass to the Python script.",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
        required=["file_path"]
    ),
)
