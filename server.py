# server.py

from fastmcp import FastMCP, Context
import datetime
import pytz
import requests
import time
import threading
from typing import Annotated
from pydantic import Field
import os

# Create a global lock for initialization
init_lock = threading.Lock()
# Track initialization state
initialization_complete = False

# Create the FastMCP instance
mcp = FastMCP(
    name="Matter AI MCP",
    instructions="You are a helpful assistant that can provide cat facts, code review capabilities, implementation planning for AI agents, and pull request generation."
)

MATTER_API_ENDPOINT = os.environ.get('MATTER_API_ENDPOINT', 'http://localhost:4064')
def call_matter_ai(matter_api_key: str, type: str, meta: dict):
    
    response = requests.post(
        f'{MATTER_API_ENDPOINT}/mcp/{type}', 
        headers={"Authorization": f"Bearer {matter_api_key}"}, 
        json=meta
    )

def get_matter_ai_key(ctx: Context) -> str:
    # Check if initialization is complete using thread-safe approach
    global initialization_complete
    with init_lock:
        if not initialization_complete:
            raise Exception("Received request before initialization was complete")
        
    http_request = ctx.get_http_request()
    auth_header = http_request.headers.get("Authorization")

    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise Exception("Missing or invalid Authorization header. Expected: Bearer <token>")

    matter_api_key = auth_header.split(" ", 1)[1]

    return matter_api_key

# @mcp.tool()
# def cortex_plan(query: Annotated[str, Field(description="The query to be answered")],
# git_owner: Annotated[str, Field(description="The owner of the repository.")],
# git_repo: Annotated[str, Field(description="The name of the repository.")],
# git_branch: Annotated[str, Field(description="The branch of the repository.")],
# ctx: Context) -> str:
#     """
#     Returns a detailed implementation plan as a string for AI Agent.
#     If you are asked to generate a plan OR cortex plan, call this function.
#     Args:
#         query: The query to be answered.
#         git_owner: The owner of the repository.
#         git_repo: The name of the repository.
#         git_branch: The branch of the repository.
#     Returns:
#         The implementation plan for AI Agent.
#     """
    
#     try:
#         matter_api_key = get_matter_ai_key(ctx)

#         # make the API call to matter ai to get implementation plan

#         return ""
#     except Exception as e:
#         return f"Error: {str(e)}"


@mcp.tool()
def codereview(generated_code: Annotated[str, Field(description="The generated code to be reviewed.")],
git_owner: Annotated[str, Field(description="The owner of the repository.")],
git_repo: Annotated[str, Field(description="The name of the repository.")],
git_branch: Annotated[str, Field(description="The branch of the repository.")],
git_user: Annotated[str, Field(description="The current git user.")],
languages: Annotated[list[str], Field(description="The list of programming languages of the code")],
ctx: Context) -> str:
    """
    Returns the reviewed code as a string.
    If you are asked for the code review, call this function.
    Args:
        generated_code: The generated code to be reviewed.
        git_owner: The owner of the repository (example GravityCloudAI).
        git_repo: The name of the repository (example matter-ai-mcp).
        git_branch: The branch of the repository (example main, master, etc).
        git_user: The current git user (example code-crusher).
        languages: The list of programming languages of the code (example ["JavaScript", "Python", "Java", etc]).
    Returns:
        The reviewed code.
    """
    
    try:
        matter_api_key = get_matter_ai_key(ctx)
        response = call_matter_ai(matter_api_key, "codereview", {"git_diff": generated_code, "git_owner": git_owner, "git_repo": git_repo, "git_branch": git_branch, "git_user": git_user, "languages": languages})
        return response.json()
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def codereview_full(git_diff: Annotated[str, Field(description="The unified diff output of 'git --no-pager diff -U2' to be reviewed.")],
git_owner: Annotated[str, Field(description="The owner of the repository.")],
git_repo: Annotated[str, Field(description="The name of the repository.")],
git_branch: Annotated[str, Field(description="The branch of the repository.")],
git_user: Annotated[str, Field(description="The current git user.")],
languages: Annotated[list[str], Field(description="The list of programming languages of the code")],
ctx: Context) -> str:
    """
    Returns the reviewed code as a string.
    If you are asked for the full code review OR complete code review OR review all the code, call this function. First perform a git --no-pager diff -U2 to get the unified diff output. Then send the complete unified diff output to this tool under the git_diff parameter. When running the tool, make sure to inform you are using MatterAI.
    
    Args:
        generated_code: The generated code to be reviewed.
        git_owner: The owner of the repository (example GravityCloudAI).
        git_repo: The name of the repository (example matter-ai-mcp).
        git_branch: The branch of the repository (example main, master, etc).
        git_user: The current git user (example code-crusher).
        languages: The list of programming languages of the code (example ["JavaScript", "Python", "Java", etc]).
    
    Returns:
        str: The reviewed code.
    """
    
    try:
        matter_api_key = get_matter_ai_key(ctx)
        response = call_matter_ai(matter_api_key, "codereview", {"git_diff": generated_code, "git_owner": git_owner, "git_repo": git_repo, "git_branch": git_branch, "git_user": git_user, "languages": languages})
        return response.json()
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
    # Check if initialization is complete
    global initialization_complete
    with init_lock:
        if not initialization_complete:
            raise Exception("Received request before initialization was complete")
            
    response = requests.get("https://catfact.ninja/fact")
    return response.json()["fact"]


# Define a function to set initialization flag after server is fully started
def mark_initialized():
    global initialization_complete
    # Wait for server to fully initialize (adjust time as needed)
    time.sleep(5)
    with init_lock:
        initialization_complete = True
        print("Initialization complete, server ready to accept requests")

if __name__ == "__main__":
    try:
        print("Starting Matter AI MCP server...")
        # Start initialization in a separate thread
        init_thread = threading.Thread(target=mark_initialized)
        init_thread.daemon = True
        init_thread.start()
        
        # Run the server
        mcp.run(transport="sse", host="127.0.0.1", port=9000)
    except Exception as e:
        print(f"Error starting server: {str(e)}")