from os.path import isfile

from google.genai import types
from config import MAX_TIME
from functions.utility import is_valid_target
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        valid, abs_working_directory, target_path = is_valid_target(
            working_directory, file_path
        )

        if not valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args:
            command.extend(map(str, args))

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=MAX_TIME,
        )

        # Return stdout and stderr combined for clarity
        output_parts = []

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stderr.strip() and not result.stdout.strip():
            output_parts.append("No output produced")

        else:
            if result.stdout.strip():
                output_parts.append(f"STDOUT:\n{result.stdout.strip()}")

            if result.stderr.strip():
                output_parts.append(f"STDERR:\n{result.stderr.strip()}")

        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return f'Error: Execution of "{file_path}" timed out after {MAX_TIME} seconds'
    except Exception as e:
        return (
            f"Error: function: run_python_file in function/ = {__name__} \n Error message = {e}"
            + f"\nError: executing Python file: {e}"
        )


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file inside the working directory with optional arguments, returning stdout and stderr.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments passed to the Python script.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)
