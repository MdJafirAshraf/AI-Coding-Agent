import subprocess
import sys
import tempfile
from pathlib import Path
from langchain_core.tools import tool

@tool
def execute_python(
    code: str,
    timeout: int = 5,
) -> dict:
    """
    Execute Python code in a temporary file.

    This tool is intended for the Tester Agent.
    It returns structured execution information.
    """

    if not code.strip():
        return {
            "status": "FAIL",
            "output": "",
            "error": "No Python code was provided.",
        }

    temp_file = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as file:

            file.write(code)
            temp_file = Path(file.name)

        result = subprocess.run(
            [sys.executable, str(temp_file)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        return {
            "status": "PASS" if result.returncode == 0 else "FAIL",
            "return_code": result.returncode,
            "output": result.stdout,
            "error": result.stderr,
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "FAIL",
            "return_code": None,
            "output": "",
            "error": f"Execution timed out after {timeout} seconds.",
        }

    except Exception as exc:
        return {
            "status": "FAIL",
            "return_code": None,
            "output": "",
            "error": str(exc),
        }

    finally:
        if temp_file and temp_file.exists():
            temp_file.unlink()