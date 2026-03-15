from os import listdir
from os.path import abspath, commonpath, getsize, isdir, join, normpath
from functions.utility import is_valid_target
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        valid_target_dir, abs_working_directory, full_target_path = is_valid_target(
            working_directory, directory
        )

        if not isdir(full_target_path):
            return f'Error: "{directory}" is not a directory'

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        contents = []
        for item in listdir(full_target_path):
            item_path = join(full_target_path, item)
            size = getsize(item_path)
            is_directory = isdir(item_path)
            contents.append(f"- {item}: file_size={size} bytes, is_dir={is_directory}")

        return "\n".join(contents)

    except Exception as e:
        return f"Error: function: get_files_info in function/ = {__name__} \n Error message =  {e}"


schema_get_files = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            )
        },
        required=["directory"],
    ),
)
