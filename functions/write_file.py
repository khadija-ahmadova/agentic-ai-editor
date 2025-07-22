import os

def write_file(working_directory, file_path, content):
    try: 
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not full_path.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # ensure parent dir exists
        parent_dir = os.path.dirname(full_path)
        os.makedirs(parent_dir, exist_ok=True)
        
        with open(full_path, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"