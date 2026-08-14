from typing import Literal
from pydantic import BaseModel, Field

class PlanStep(BaseModel):
    step_number: int = Field(description="Sequential number of the implementation step.")
    description: str = Field(description="What needs to be implemented in this step.")


class PlanResponse(BaseModel):
    goal: str = Field(description="Short description of what the user wants.")
    steps: list[PlanStep] = Field(description="Ordered implementation steps.")


class CodeResponse(BaseModel):
    code: str = Field(description="Complete executable Python code.")
    language: Literal["python"] = Field(description="Programming language of the generated code.")
    explanation: str = Field(description="Short explanation of the generated program.")


class TestResponse(BaseModel):
    status: Literal["PASS", "FAIL"] = Field(description="Whether the generated Python code passed testing.")
    syntax_valid: bool = Field(description="Whether the Python code has valid syntax.")
    execution_valid: bool = Field(description="Whether the Python code executed successfully.")
    output: str = Field(default="", description="Captured program output.")
    errors: list[str] = Field(default_factory=list, description="Errors found while validating or executing the code.")
    summary: str = Field(description="Short summary of the test result.")


class ReviewResponse(BaseModel):
    status: Literal["PASS", "FAIL"] = Field(description="Whether the code satisfies the requirement.")
    requirement_met: bool = Field(description="Whether the implementation satisfies the user requirement.")
    issues: list[str] = Field(default_factory=list, description="Problems found in the implementation.")
    suggestions: list[str] = Field(default_factory=list, description="Suggested improvements or corrections.")
    summary: str = Field(description="Short review summary.")