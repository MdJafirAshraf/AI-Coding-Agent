def validate_python_syntax(code: str) -> dict:
    """
    Validate Python syntax without executing the code.
    """

    if not code.strip():
        return {
            "valid": False,
            "error": "No Python code was provided.",
        }

    try:
        compile(
            code,
            "<generated_code>",
            "exec",
        )

        return {
            "valid": True,
            "error": None,
        }

    except SyntaxError as exc:
        return {
            "valid": False,
            "error": (
                f"SyntaxError: {exc.msg} "
                f"(line {exc.lineno})"
            ),
        }

    except Exception as exc:
        return {
            "valid": False,
            "error": str(exc),
        }