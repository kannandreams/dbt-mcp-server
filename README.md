# 🛠️ dbt MCP Server
This is a minimal, extensible MCP (Model Control Protocol) server to run dbt models with a unified interface.

## Overview
A unified JSON-based workflow for triggering dbt models, tests, and other dbt operations, triggered via CLI, API, or an AI interface like Claude. Includes Slack notifications for task completions.


## 🚀 Getting Started

✅ Ready to plug into AI tools like Claude for prompt-driven automation!

### Run Locally with UV
```bash
uvicorn mcp_dispatcher:app --reload --port 8000
```

### Run with Docker
```bash
docker build -t dbt-mcp-server .
docker run -p 8000:8000 dbt-mcp-server
```

### 5. Trigger MCP from Claude (supported client)
```bash
python claude_client_example.py
```

## 📣 Slack Alerts
Set your `SLACK_WEBHOOK_URL` to get alerts on model success or failure.

## 🔌 Usage

```bash
python mcp_dispatcher.py mcp_request.json
```

```
{
  "mcpServers": {
    "fetch": {
      "command": "node",
      "args": [
        "{ABSOLUTE PATH TO FILE HERE}/dist/index.js"
      ]
    }
  }
}
```

## Features
- Run dbt models using a clean JSON spec
- Accept CLI or HTTP API calls
- Slack alerts for model status
- Compatible with Claude

## 🛠️ Contributing
If you're interested in contributing, feel free to open an issue to start a discussion or directly submit a pull request. Whether it's code, ideas, or feedback—all contributions are welcome!

### License
This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
