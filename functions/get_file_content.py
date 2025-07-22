import os
MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        # print(working_directory)
        # print(file_path)
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        # print(working_directory)
        # print(file_path)

        if not full_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(full_path, "r", encoding="utf-8") as file:
            file_content_string = file.read()
        if len(file_content_string) > MAX_CHARS:
            file_content_string = file_content_string[:MAX_CHARS] + f'\n[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string

    except Exception as e:
        return f"Error: {e}"