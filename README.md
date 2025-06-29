<div align="center">
  <a href="https://matterai.so">
    <img
      src="https://matterai.so/favicon.png"
      alt="Matter AI Logo"
      height="64"
    />
  </a>
  <br />
  <p>
    <h3>
      <b>
        Matter AI
      </b>
    </h3>
  </p>
  <p>
    <b>
      Release Code with Confidence. Everytime.
    </b>
  </p>
  <p>

![Matter Og Image](https://res.cloudinary.com/dxvbskvxm/image/upload/v1751168720/ph-header_cy8iqj.png)

  </p>
</div>


# Matter AI MCP Server

A powerful MCP (Model Context Protocol) server for Cursor, Windsurf, and other AI clients that enhances your development workflow. Built with [FastMCP](https://github.com/modelcontextprotocol/fastmcp) in Python, it provides advanced code review capabilities, implementation planning, and pull request generation to help you release code with confidence.

## Features
- **Code review tools** - Get comprehensive code reviews for individual files or full git diffs
- **Implementation planning** - Generate detailed implementation plans for AI agents
- **Pull request generation** - Create pull requests with auto-generated titles and descriptions
- **Random cat facts** - Because who doesn't love cat facts?

## Requirements
- Python 3.11+
- See `requirements.txt` for dependencies

## Installation
```bash
pip install -r requirements.txt
```

## Setup

### API Key
To use Matter AI MCP Server, you need an API key:
1. Obtain your API key from [https://app.matterai.dev/settings](https://app.matterai.dev/settings)
2. Use this key in your MCP configuration as shown below

### MCP Configuration
Create an MCP configuration file with the following content:

```json
{
  "mcpServers": {
    "matter-ai": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcplocal.matterai.dev/sse",
        "--header",
        "Authorization: Bearer MATTER_AI_API_KEY"
      ]
    }
  }
}
```

Replace `MATTER_AI_API_KEY` with your actual API key.

## Usage
Run the server:
```bash
python server.py
```
The server will start on `http://localhost:9000` (default for FastMCP).

### Connecting from Cursor or Windsurf
- Use the MCP (Model Context Protocol) integration
- Point to: `http://localhost:9000/sse`
- Tools will auto-discover and appear in the client

## Tools
### 1. `cat_fact() -> str`
Returns a random cat fact.

### 2. `codereview(generated_code: str, git_owner: str, git_repo: str, git_branch: str, git_user: str, languages: str) -> str`
Provides code review for the generated code.

### 3. `codereview_full(git_diff: str, git_owner: str, git_repo: str, git_branch: str, git_user: str) -> str`
Provides a comprehensive code review based on git diff output.

### 4. `cortex_plan(query: str, git_owner: str, git_repo: str, git_branch: str) -> str`
Generates a detailed implementation plan for AI Agent.

### 5. `generate_pull_request(source_branch: str, current_branch: str, git_owner: str, git_repo: str, git_branch: str, git_user: str) -> dict`
Creates a pull request with auto-generated title and description.
---

## License
MIT
