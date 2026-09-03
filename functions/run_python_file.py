import os
import subprocess
from google.genai import types

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file_path]
        if args:
            command.extend(args)
        completed_process = subprocess.run(command, capture_output=True, timeout=30, text=True, cwd=working_dir_abs)
        output_string = []
        if completed_process.returncode != 0:
            output_string.append(f"Process exited with code {completed_process.returncode}")
        if not completed_process.stderr and not completed_process.stdout:
            output_string.append("No output produced")
        if completed_process.stdout:
            output_string.append(f"STDOUT: {completed_process.stdout}")
        if completed_process.stderr:
            output_string.append(f"STDERR: {completed_process.stderr}")
        final_string = "\n".join(output_string)    
        return final_string
    except Exception as error:
        return f"Error: executing Python file: {error}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Takes a specified file from a specified working directory, attempting to run/execute the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to execute, relative to the working directory",
            ),

            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the Python file",
            )
        },
        required=["file_path"]
    ),
)
        


