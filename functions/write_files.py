from os import makedirs
from os.path import dirname, isdir, join, normcase
from functions.utility import is_valid_target
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        valid_target_file, abs_working_directory, target_path = is_valid_target(
            working_directory, file_path
        )

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = dirname(target_path)
        makedirs(parent_dir, exist_ok=True)

        with open(target_path, "w", encoding="utf-8") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: function: write_file in function/ = {__name__} \n Error message =  {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to a file inside the working directory, creating parent directories if needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
