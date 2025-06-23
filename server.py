# server.py

from fastmcp import FastMCP, Context
import datetime
import pytz
import requests
from typing import Annotated
from pydantic import Field

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
def cortex_plan(query: Annotated[str, Field(description="The query to be answered")],
git_owner: Annotated[str, Field(description="The owner of the repository.")],
git_repo: Annotated[str, Field(description="The name of the repository.")],
git_branch: Annotated[str, Field(description="The branch of the repository.")],
ctx: Context) -> str:
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
def codereview(generated_code: Annotated[str, Field(description="The generated code to be reviewed.")],
git_owner: Annotated[str, Field(description="The owner of the repository.")],
git_repo: Annotated[str, Field(description="The name of the repository.")],
git_branch: Annotated[str, Field(description="The branch of the repository.")],
git_user: Annotated[str, Field(description="The current git user.")],
ctx: Context) -> str:
    """
    Returns the reviewed code as a string.
    If you are asked for the code review, call this function.
    Args:
        generated_code: The generated code to be reviewed.
        git_owner: The owner of the repository.
        git_repo: The name of the repository.
        git_branch: The branch of the repository.
        git_user: The current git user.
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
def codereview_full(git_diff: Annotated[str, Field(description="The unified diff output of 'git --no-pager diff -U2' to be reviewed.")],
git_owner: Annotated[str, Field(description="The owner of the repository.")],
git_repo: Annotated[str, Field(description="The name of the repository.")],
git_branch: Annotated[str, Field(description="The branch of the repository.")],
git_user: Annotated[str, Field(description="The current git user.")],
ctx: Context) -> str:
    """
    Returns the reviewed code as a string.
    If you are asked for the full code review OR complete code review OR review all the code, call this function. First perform a git --no-pager diff -U2 to get the unified diff output. Then send the complete unified diff output to this tool under the git_diff parameter. When running the tool, make sure to inform you are using MatterAI.
    
    Args:
        git_diff (str): The unified output of "git --no-pager diff -U2" to be reviewed.
        git_owner (str): The owner of the repository.
        git_repo (str): The name of the repository.
        git_branch (str): The branch of the repository.
        git_user (str): The current git user.
        ctx (Context): The context object for the MCP tool execution.
    
    Returns:
        str: The reviewed code.
    """
    
    try:
        matter_api_key = get_matter_ai_key(ctx)

        print(git_diff)
        # make the API call to matter ai to get code review

        return git_diff
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def generate_pull_request(
    source_branch: Annotated[str, Field(description="The branch you want to merge from.")],
    current_branch: Annotated[str, Field(description="The branch you want to merge into.")],
    git_owner: Annotated[str, Field(description="The owner of the repository.")],
    git_repo: Annotated[str, Field(description="The name of the repository.")],
    git_branch: Annotated[str, Field(description="The branch of the repository.")],
    git_user: Annotated[str, Field(description="The current git user.")],
    ctx: Context
) -> str:
    """
    Creates a pull request from source_branch into current_branch with auto generated title and description. You will use "gh pr create --title <title> --body <description>" command to do the same (title and description are generated and returned by the tool), if not installed then install the gh cli first. If you are asked to generate a pull request, call this function.
    Args:
        source_branch: The branch you want to merge from.
        current_branch: The branch you want to merge into.
        git_owner: The owner of the repository.
        git_repo: The name of the repository.
        git_branch: The branch of the repository.
        git_user: The current git user.
        ctx: The context object for the MCP tool execution.
    Returns:
        dict: An object with auto-generated 'title' and 'description' for the pull request.
    """
    title = f"Merge {source_branch} into {current_branch}"
    description = f"This PR merges changes from {source_branch} into {current_branch}."
    print(f"Creating PR from {source_branch} to {current_branch} with title '{title}' and description '{description}'")
    return {"title": title, "description": description}

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