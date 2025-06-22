# server.py

from fastmcp import FastMCP, Context
import datetime
import pytz
import requests

mcp = FastMCP(
    name="Matter AI MCP",
    instructions="You are a helpful assistant that can provide information about the current date and time, as well as cat facts."
)

def get_matter_ai_key(ctx: Context) -> str:
    http_request = ctx.get_http_request()
    auth_header = http_request.headers.get("Authorization")

    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise Exception("Missing or invalid Authorization header. Expected: Bearer <token>")

    matter_api_key = auth_header.split(" ", 1)[1]

    print(f"Received API Key from Auth Header: {matter_api_key}")

    return matter_api_key

@mcp.tool()
def cortex_plan(query: str, git_owner: str, git_repo: str, git_branch: str, ctx: Context) -> str:
    """
    Returns a detailed implementation plan as a string for AI Agent.
    If you are asked to generate a plan OR cortex plan, call this function.
    Args:
        query: The query to be answered.
        git_owner: The owner of the repository.
        git_repo: The name of the repository.
        git_branch: The branch of the repository.
    Returns:
        The implementation plan for AI Agent.
    """
    
    try:
        matter_api_key = get_matter_ai_key(ctx)

        # make the API call to matter ai to get implementation plan

        return ""
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def codereview(generated_code: str, git_owner: str, git_repo: str, git_branch: str, ctx: Context) -> str:
    """
    Returns the reviewed code as a string.
    If you are asked for the code review, call this function.
    Args:
        generated_code: The generated code to be reviewed.
        git_owner: The owner of the repository.
        git_repo: The name of the repository.
        git_branch: The branch of the repository.
    Returns:
        The reviewed code.
    """
    
    try:
        matter_api_key = get_matter_ai_key(ctx)

        # make the API call to matter ai to get code review

        return generated_code
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def codereview_full(git_diff: str, git_owner: str, git_repo: str, git_branch: str, ctx: Context) -> str:
    """
    Returns the reviewed code as a string.
    If you are asked for the full code review OR complete code review OR review all the code, call this function.
    Args:
        git_diff: The git diff to be reviewed.
        git_owner: The owner of the repository.
        git_repo: The name of the repository.
        git_branch: The branch of the repository.
    Returns:
        The reviewed code.
    """
    
    try:
        matter_api_key = get_matter_ai_key(ctx)

        # make the API call to matter ai to get code review

        return git_diff
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def cat_fact() -> str:
    """
    Returns a random cat fact.
    If you are asked for a cat fact, call this function.
    Args:
        None
    Returns:
        A random cat fact.
    """
    response = requests.get("https://catfact.ninja/fact")
    return response.json()["fact"]


if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=9000)