from tools import execute_python, validate_python_syntax


code = """
numbers = [10, 20, 30]

total = sum(numbers)
average = total / len(numbers)

print("Total:", total)
print("Average:", average)
"""


print("=== SYNTAX VALIDATION ===")

syntax_result = validate_python_syntax(code)

print(syntax_result)


print("\n=== CODE EXECUTION ===")

execution_result = execute_python(code)

print(execution_result)