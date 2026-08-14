from tools import execute_python, validate_python_syntax


code = """
def calculate_average(numbers):
    if not numbers:
        return 0
    total = sum(numbers)
    average = total / len(numbers)
    return total, average

if __name__ == "__main__":
    numbers = [10, 20, 30, 40, 50]
    total, average = calculate_average(numbers)
    print(f"Total: {total}")
    print(f"Average: {average}")
"""


print("=== SYNTAX VALIDATION ===")

syntax_result = validate_python_syntax(code)

print(syntax_result)


print("\n=== CODE EXECUTION ===")

execution_result = execute_python(code)

print(execution_result)