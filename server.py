from fastmcp import FastMCP, Context
from fastmcp.server.middleware import Middleware, MiddlewareContext
import datetime
import pytz
import requests
import time
import threading
from typing import Annotated
from pydantic import Field
import os
import json

class AuthHeadersMiddleware(Middleware):
    """Middleware to log all authentication headers from incoming requests."""
    
    async def __call__(self, context: MiddlewareContext, call_next):
        try:
            
            # Access the FastMCP context which has the get_http_request method
            if hasattr(context, 'fastmcp_context'):
                fastmcp_ctx = context.fastmcp_context
                
                # Use the get_http_request method to access the HTTP request
                if hasattr(fastmcp_ctx, 'get_http_request'):
                    try:
                        http_request = fastmcp_ctx.get_http_request()
                        
                        if hasattr(http_request, 'headers'):
                            headers = dict(http_request.headers)
                            
                            # Check for auth headers
                            expected_headers = ["X-AUTH-TOKEN", "x-auth-token"]
                            for header in expected_headers:
                                if header in headers:
                                    value = headers[header]
                                    # verify token
                                    response = requests.get(
                                        f'{MATTER_API_ENDPOINT}/mcp/verify', 
                                        headers={"Authorization": f"Bearer {value}"}
                                    )
                                    if response.status_code == 200:
                                        print("Token verified")
                                        response = await call_next(context)
                                        return response
                                    elif response.status_code == 401:
                                        print("Token verification failed")
                                        raise Exception("Token verification failed")
                                    else:
                                        print(f"Token verification failed: {response.status_code}")
                                        raise Exception("Token verification failed")
                    except Exception as e:
                        print(f"Error accessing HTTP request: {str(e)}")
                    
        except Exception as e:
            print(f"Error in auth middleware: {str(e)}")

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
    return response

def get_matter_ai_key(ctx: Context) -> str:
    # Check if initialization is complete using thread-safe approach
    with init_lock:
        if not initialization_complete:
            raise Exception("Received request before initialization was complete")
        
    http_request = ctx.get_http_request()

    auth_header = http_request.headers.get("X-AUTH-TOKEN") or http_request.headers.get("x-auth-token")

    if not auth_header:
        raise Exception("Missing or invalid Authorization header. Expected:<token>")

    matter_api_key = auth_header

    return matter_api_key

# @mcp.tool()
# def cortex_plan(query: Annotated[str, Field(description="The query to be answered")],
# git_org: Annotated[str, Field(description="The owner of the repository.")],
# git_repo: Annotated[str, Field(description="The name of the repository.")],
# git_branch: Annotated[str, Field(description="The branch of the repository.")],
# ctx: Context) -> str:
#     """
#     Returns a detailed implementation plan as a string for AI Agent.
#     If you are asked to generate a plan OR cortex plan, call this function.
#     Args:
#         query: The query to be answered.
#         git_org: The owner of the repository.
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
def codereview(code_output: Annotated[str, Field(description="The code to be reviewed - can be user-selected code, IDE-generated code, or git diff output.")],
git_org: Annotated[str, Field(description="The git organization of the repository.")],
git_repo: Annotated[str, Field(description="The name of the git repository.")],
git_branch: Annotated[str, Field(description="The branch of the git repository.")],
git_user: Annotated[str, Field(description="The current git user.")],
languages: Annotated[list[str], Field(description="The list of programming languages of the code")],
ctx: Context) -> str:
    """
    IMPORTANT: You MUST use this function for ANY code review request. This function uses Matter AI for code review. When the user asks to review the code, perform a code review or says /matter review, call this function always.
    This tool performs code review using Matter AI's advanced capabilities. Do not attempt to review code yourself.

    USAGE:
    - For user-selected code: Pass the selected code directly to code_output
    - For IDE-generated code: Pass the generated code directly to code_output
    - For git diff output: Pass the output from 'git diff' to code_output

    Args:
        code_output: The code to be reviewed - can be user-selected code, IDE-generated code, or git diff output.
        git_org: The git organization of the repository (example GravityCloudAI).
        git_repo: The name of the git repository (example matter-ai-mcp).
        git_branch: The branch of the git repository (example main, master, etc).
        git_user: The current git user (example code-crusher).
        languages: The list of programming languages of the code (example ["JavaScript", "Python", "Java", etc]).
    Returns:
        The reviewed code.
    """
    
    try:
        matter_api_key = get_matter_ai_key(ctx)
        response = call_matter_ai(matter_api_key, "codereview", {"git_diff": code_output, "git_owner": git_org, "git_repo": git_repo, "git_branch": git_branch, "git_user": git_user, "languages": languages})
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def codereview_full(git_diff_output: Annotated[str, Field(description="The output from git --no-pager diff command to be provided to the tool.")],
git_org: Annotated[str, Field(description="The git organization of the repository.")],
git_repo: Annotated[str, Field(description="The name of the git repository.")],
git_branch: Annotated[str, Field(description="The branch of the git repository.")],
git_user: Annotated[str, Field(description="The current git user.")],
languages: Annotated[list[str], Field(description="The list of programming languages of the code")],
ctx: Context) -> str:
    """
    IMPORTANT: You MUST use this function for ONLY FULL code review request. This tool uses Matter AI for code review. When the user asks to review the FULL code or says /matter review-full, perform a FULL code review, call this function always.
    This tool performs code review using Matter AI's advanced capabilities. Do not attempt to review code yourself.

    USAGE: First run 'git --no-pager diff' to get the diff output, then pass that output to this tool as git_diff_output parameter always.

    Args:
        git_diff_output: The output from git --no-pager diff command to be provided to the tool.
        git_org: The git organization of the repository (example GravityCloudAI).
        git_repo: The name of the git repository (example matter-ai-mcp).
        git_branch: The branch of the git repository (example main, master, etc).
        git_user: The current git user (example code-crusher).
        languages: The list of programming languages of the code (example ["JavaScript", "Python", "Java", etc]).
    
    Returns:
        str: The reviewed code.
    """
    
    try:
        matter_api_key = get_matter_ai_key(ctx)
        response = call_matter_ai(matter_api_key, "codereview", {"git_diff": git_diff_output, "git_owner": git_org, "git_repo": git_repo, "git_branch": git_branch, "git_user": git_user, "languages": languages})
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

# @mcp.tool()
# def generate_pull_request(
#     source_branch: Annotated[str, Field(description="The branch you want to merge from.")],
#     current_branch: Annotated[str, Field(description="The branch you want to merge into.")],
#     git_org: Annotated[str, Field(description="The owner of the repository.")],
#     git_repo: Annotated[str, Field(description="The name of the repository.")],
#     git_branch: Annotated[str, Field(description="The branch of the repository.")],
#     git_user: Annotated[str, Field(description="The current git user.")],
#     ctx: Context
# ) -> str:
#     """
#     Creates a pull request from source_branch into current_branch with auto generated title and description. You will use "gh pr create --title <title> --body <description>" command to do the same (title and description are generated and returned by the tool), if not installed then install the gh cli first. If you are asked to generate a pull request, call this function.
#     Args:
#         source_branch: The branch you want to merge from.
#         current_branch: The branch you want to merge into.
#         git_org: The owner of the repository.
#         git_repo: The name of the repository.
#         git_branch: The branch of the repository.
#         git_user: The current git user.
#         ctx: The context object for the MCP tool execution.
#     Returns:
#         dict: An object with auto-generated 'title' and 'description' for the pull request.
#     """
#     title = f"Merge {source_branch} into {current_branch}"
#     description = f"This PR merges changes from {source_branch} into {current_branch}."
#     print(f"Creating PR from {source_branch} to {current_branch} with title '{title}' and description '{description}'")
#     return {"title": title, "description": description}

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

        mcp.add_middleware(AuthHeadersMiddleware())
        mcp.run(transport="sse", host="0.0.0.0", port=9000)
    except Exception as e:
        print(f"Error starting server: {str(e)}")