import os
MAX_CHARS = 10000

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        working_directory = os.path.abspath(working_directory)

        if not full_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        content_list = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            content_list.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(content_list)
    
    except Exception as e:
        return f"Error: {e}"

    
def get_file_content(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(file_path)

        if not file_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(file_path, "r", encoding="utf-8") as file:
            file_content_string = file.read()
        if len(file_content_string) > MAX_CHARS:
            content = content[:MAX_CHARS] + f'\n[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string

    except Exception as e:
        return f"Error: {e}"