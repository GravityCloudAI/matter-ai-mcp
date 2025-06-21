# Matter AI MCP Server

A minimal MCP (Model Context Protocol) server for Cursor, Windsurf, and other AI clients. Built with [FastMCP](https://github.com/modelcontextprotocol/fastmcp) in Python, it exposes tools for getting the current date/time and random cat facts.

## Features
- **get current date and time** (with timezone support)
- **get a random cat fact**
- Simple code review tool (echoes code)

## Requirements
- Python 3.11+
- See `requirements.txt` for dependencies

## Installation
```bash
pip install -r requirements.txt
```

## Usage
Run the server:
```bash
python server.py
```
The server will start on `http://localhost:8000` (default for FastMCP).

### Connecting from Cursor or Windsurf
- Use the MCP (Model Context Protocol) integration.
- Point to: `http://localhost:8000/sse`
- Tools will auto-discover and appear in the client.

## Tools
### 1. `current_datetime(timezone: str = "America/New_York") -> str`
Returns the current date and time in the specified timezone.

### 2. `cat_fact() -> str`
Returns a random cat fact from catfact.ninja.

### 3. `codereview(generated_code: str) -> str`
Echoes the provided code (placeholder for code review logic).
---

## License
MIT
