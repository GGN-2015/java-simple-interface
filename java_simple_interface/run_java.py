import os
import subprocess
from typing import List, Dict, Optional

try:
    from .java_version import java_exists
except:
    from java_version import java_exists

def run_java_in_dir(
        target_dir: str, 
        java_command: List[str], 
        encoding:str) -> Dict[str, Optional[str | int]]:

    """
    Execute a custom Java command in a specified directory, and switch back to the original working directory
    regardless of whether the command succeeds or fails.
    
    Args:
        target_dir: The directory where the Java command will be executed
        java_command: List of Java command arguments (e.g., ["-jar", "myapp.jar", "arg1"])
    
    Returns:
        Dictionary containing execution results:
            - original_cwd: Original working directory (for verification)
            - target_cwd: Target execution directory
            - return_code: Command exit code (0 = success, non-0 = failure)
            - stdout: Standard output of the command (string)
            - stderr: Standard error of the command (string)
            - error: Exception message if any (e.g., directory not found)
    """
    # Initialize result dictionary
    result: Dict[str, Optional[str | int]] = {
        "original_cwd": os.getcwd(),
        "target_cwd": target_dir,
        "return_code": None,
        "stdout": None,
        "stderr": None,
        "error": None
    }

    try:
        if not java_exists():
            raise RuntimeError("java not found.")

        # Step 1: Switch to target directory
        os.chdir(target_dir)
        
        # Step 2: Execute Java command via subprocess
        proc = subprocess.run(
            ["java"] + java_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding=encoding
        )
        
        # Record command execution results
        result["return_code"] = proc.returncode
        result["stdout"] = proc.stdout if proc.stdout else ""
        result["stderr"] = proc.stderr if proc.stderr else ""

    except FileNotFoundError as e:
        # Handle case where java command or target file is not found
        result["error"] = f"File not found error: {str(e)}. Check if Java is installed or target file exists."
    except NotADirectoryError as e:
        # Handle case where target_dir is not a valid directory
        result["error"] = f"Invalid directory: {str(e)}. Target path is not a directory."
    except PermissionError as e:
        # Handle permission issues (e.g., cannot access directory/run Java)
        result["error"] = f"Permission error: {str(e)}. Check directory/file permissions."
    except Exception as e:
        # Catch all other unexpected errors
        result["error"] = f"Unexpected error: {str(e)}"
    finally:
        # Critical: Switch back to original directory NO MATTER WHAT
        os.chdir(str(result["original_cwd"]))

    return result
