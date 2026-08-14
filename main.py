from PIL import Image
from io import BytesIO
from deepagents import create_deep_agent
from langchain_groq import ChatGroq
from langchain_core.rate_limiters import InMemoryRateLimiter

from prompts import MAIN_AGENT_PROMPT, PLANNER_AGENT_PROMPT, CODER_AGENT_PROMPT, TESTER_AGENT_PROMPT, REVIEWER_AGENT_PROMPT
from schemas import PlanResponse, CodeResponse, TestResponse, ReviewResponse
from middleware import LoggingMiddleware, IterationGuardMiddleware
from tools.python_executor import execute_python
from tools.python_validator import validate_python_syntax

from dotenv import load_dotenv
load_dotenv()

# Model
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.15,
    check_every_n_seconds=0.5,
    max_bucket_size=1,
)

model = ChatGroq(
    model="openai/gpt-oss-120b", 
    temperature=0,
    # max_output_tokens=768,
    # rate_limiter=rate_limiter,
)


# Subagent
planner_agent = {
    "name": "planner",
    "description": (
        "Creates a concise implementation plan for Python "
        "coding tasks. Use this agent when a coding request "
        "requires multiple implementation steps or clear "
        "requirements decomposition."
    ),
    "system_prompt": PLANNER_AGENT_PROMPT,
    # "response_format": PlanResponse,
    "middleware": [LoggingMiddleware(agent_name="planner")],
}


coder_agent = {
    "name": "coder",
    "description": (
        "Generates complete single-file Python code from "
        "a user requirement and implementation plan. "
        "Use this agent when Python code needs to be created "
        "or corrected."
    ),
    "system_prompt": CODER_AGENT_PROMPT,
    # "response_format": CodeResponse,
    "middleware": [LoggingMiddleware(agent_name="coder")],
}


tester_agent = {
    "name": "tester",
    "description": (
        "Tests generated Python code by checking syntax "
        "and executing the code. Use this agent to verify "
        "whether generated code actually runs."
    ),
    "system_prompt": TESTER_AGENT_PROMPT,
    "tools": [
        validate_python_syntax,
        execute_python,
    ],
    # "response_format": TestResponse,
    "middleware": [LoggingMiddleware(agent_name="tester")],
}


reviewer_agent = {
    "name": "reviewer",
    "description": (
        "Reviews generated Python code against the user's "
        "requirements and tester results. Use this agent "
        "to identify semantic, completeness, and requirement "
        "violations."
    ),
    "system_prompt": REVIEWER_AGENT_PROMPT,
    # "response_format": ReviewResponse,
    "middleware": [LoggingMiddleware(agent_name="reviewer")],
}


# Main Agent
deep_agent = create_deep_agent(
    model=model,
    system_prompt=MAIN_AGENT_PROMPT,
    middleware=[LoggingMiddleware(agent_name="main"), IterationGuardMiddleware(max_iterations=3)],
    subagents=[planner_agent, coder_agent, tester_agent, reviewer_agent],
)

def show_graph() -> None:
    """Render the agent graph. Only called with --debug, not on every run."""
    from PIL import Image

    img_bytes = deep_agent.get_graph(xray=True).draw_mermaid_png()
    img = Image.open(BytesIO(img_bytes))
    img.show()


# Run Agent
result = deep_agent.invoke(
    {"messages": [{
        "role": "user",
        "content": (
            "Create a Python program that calculates "
            "the sum and average of a list of numbers."
        ),
    }]}
)

# show_graph()
