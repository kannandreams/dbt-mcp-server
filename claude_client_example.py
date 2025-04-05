# claude_client_example.py
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

user_prompt = "Run the customer_lifetime_value model in production with full refresh and 2 threads."

headers = {
    "x-api-key": CLAUDE_API_KEY,
    "anthropic-version": "2023-06-01",
    "Content-Type": "application/json"
}

with open("prompt_templates/dbt_prompt_template.txt") as f:
    template = f.read()

prompt_template = template.replace("{user_prompt}", user_prompt)

response = requests.post(
    CLAUDE_API_URL,
    headers=headers,
    json={
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 500,
        "temperature": 0,
        "messages": [
            {"role": "user", "content": prompt_template}
        ]
    }
)

response_data = response.json()
completion_text = response_data["content"][0]["text"]
claude_generated_mcp = json.loads(completion_text)

with open("mcp_servers.json") as f:
    mcp_servers = json.load(f)["mcpServers"]

tool = claude_generated_mcp["tool"]
server_info = mcp_servers.get(tool)
if not server_info:
    raise Exception(f"No MCP server configured for tool '{tool}'")

mcp_response = requests.post(
    server_info["url"],
    headers={"Content-Type": "application/json"},
    json=claude_generated_mcp
)

print("Response:", mcp_response.status_code)
print(mcp_response.json())