# claude_client_example.py
import json
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

print("\n")
print("👋 Hey there! I am your 🤖 Data Engineer Assistant (powered by Claude).")
print("\n")
print("💡 I can help you with the following tasks:")
print("1. Generate a dbt model")
print("2. Run a dbt model")
print("3. Test a dbt model")
print("4. Document a dbt model")
input("🔍 Please select a task (1-4): ")
print("\n")
print("📝 Please provide a description of the task you want to perform.")
user_prompt = input("🗣️ Your description: ")

with open("prompt_templates/dbt_prompt_template.txt") as f:
    prompt_template = f.read()

formatted_prompt = prompt_template.replace("{user_prompt}", user_prompt)

headers = {
    "x-api-key": CLAUDE_API_KEY,
    "anthropic-version": "2023-06-01",
    "Content-Type": "application/json"
}

response = requests.post(
    CLAUDE_API_URL,
    headers=headers,
    json={
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 500,
        "temperature": 0,
        "messages": [
            {"role": "user", "content": formatted_prompt}
        ]
    }
)

response_data = response.json()
completion_text = response_data["content"][0]["text"]
print("\n🧠 Claude Response:")
print(completion_text)

claude_generated_mcp = json.loads(completion_text)

# Highlight extracted values
print("\n🔍 Extracted MCP Payload:")
print(f"🔧 Tool: {claude_generated_mcp['tool']}")
print(f"⚙️  Action: {claude_generated_mcp['action']}")
print(f"📦 Model Name: {claude_generated_mcp['payload'].get('model_name')}")
print(f"🛠️  Full Refresh: {claude_generated_mcp['payload']['flags'].get('full_refresh')}")
print(f"🧵 Threads: {claude_generated_mcp['payload']['flags'].get('threads')}")

# Load mcpServers config
with open("mcp_servers.json") as f:
    mcp_servers = json.load(f)["mcpServers"]

tool = claude_generated_mcp["tool"]
server_info = mcp_servers.get(tool)
if not server_info:
    raise Exception(f"No MCP server configured for tool '{tool}'")

# Trigger MCP Server
mcp_response = requests.post(
    server_info["url"],
    headers={"Content-Type": "application/json"},
    json=claude_generated_mcp
)

print("\n🚀 MCP Server Response:")
print("Status Code:", mcp_response.status_code)
print(mcp_response.json())