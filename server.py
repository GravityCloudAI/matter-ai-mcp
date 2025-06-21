# server.py

from fastmcp import FastMCP
import datetime
import pytz
import requests

mcp = FastMCP(
    name="Matter AI MCP",
    instructions="You are a helpful assistant that can provide information about the current date and time, as well as cat facts."
)

@mcp.tool()
def codereview(generated_code: str) -> str:
    """
    Returns the reviewed code as a string. 
    If you are asked for the code review, call this function.
    Args:
        generated_code: The generated code to be reviewed.
    Returns:
        The reviewed code.
    """
    
    try:
        return generated_code
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