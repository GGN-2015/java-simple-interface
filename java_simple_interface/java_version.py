import subprocess
from typing import Dict, Optional

def check_java_availability() -> Dict[str, Optional[str | bool]]:
    """
    Check if Java is available in the command line environment by running `java -version`.
    All output/error information is returned as a dictionary (no direct console printing).
    
    Returns:
        Dict[str, Optional[str | bool]]: Structured result with the following keys:
            - "status": True if Java is available, False otherwise (boolean)
            - "version_details": Full Java version output (string, only if status=True)
            - "error_message": Error description (string, only if status=False)
    """
    result: Dict[str, Optional[str | bool]] = {
        "status": False,  # Default to False (unavailable)
        "version_details": None,
        "error_message": None
    }

    try:
        # Execute `java -version` command
        proc = subprocess.run(
            ["java", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            encoding="utf-8"
        )

        # `java -version` outputs version info to stderr (standard behavior)
        java_version_info = proc.stderr.strip()
        result["status"] = True  # Update to True (available)
        result["version_details"] = java_version_info

    except subprocess.CalledProcessError as e:
        # Non-zero exit code (Java command exists but failed to execute)
        error_detail = e.stderr.strip() if e.stderr else "Java command returned non-zero exit code"
        result["error_message"] = f"Java execution failed: {error_detail}"

    except FileNotFoundError:
        # `java` command not found in system PATH
        result["error_message"] = "'java' command not found in PATH. Java is not installed or misconfigured."

    except Exception as e:
        # Catch all other unexpected errors
        result["error_message"] = f"Unexpected error checking Java: {str(e)}"

    return result

def java_exists() -> bool:
    return bool(check_java_availability()["status"])

# Example usage (printing is optional and controlled here)
if __name__ == "__main__":
    java_check_result = check_java_availability()
    
    # Customize output based on the returned boolean status
    if java_check_result["status"]:
        print("Java is available!")
        print(f"Version Details:\n{java_check_result['version_details']}")
    else:
        print("Java is unavailable.")
        print(f"Error: {java_check_result['error_message']}")
