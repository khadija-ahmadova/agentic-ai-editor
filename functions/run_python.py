import os
import subprocess

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