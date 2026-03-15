from os.path import abspath, commonpath, isfile, join, normcase
from config import MAX_CHARS
from functions.utility import is_valid_target
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        valid_target_file, abs_working_directory, target_path = is_valid_target(
            working_directory, file_path
        )

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)
            if file.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

            return file_content_string

    except Exception as e:
        return f"Error: function: get_file_content in function/ = {__name__} \n Error message =  {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the content of a file within the working directory, truncated to {MAX_CHARS} if too large.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory.",
            )
        },
        required=["file_path"],
    ),
)
