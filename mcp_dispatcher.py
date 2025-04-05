import json
import subprocess
import sys
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MCP Dispatcher for dbt")

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

class MCPPayload(BaseModel):
    mcp_version: str
    tool: str
    action: str
    payload: dict
    metadata: dict = {}

def run_dbt_model(payload):
    model = payload["model_name"]
    flags = payload.get("flags", {})
    variables = payload.get("variables", {})

    cmd = ["dbt", "run", "--select", model]

    if flags.get("full_refresh"):
        cmd.append("--full-refresh")
    if flags.get("threads"):
        cmd.extend(["--threads", str(flags["threads"])])

    if variables:
        vars_str = json.dumps(variables)
        cmd.extend(["--vars", vars_str])

    print("Running command:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr

def notify_slack(message):
    payload = {"text": message}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code != 200:
            print("Slack notification failed:", response.text)
    except Exception as e:
        print("Slack notification error:", str(e))

def handle_mcp_request(mcp_data):
    tool = mcp_data.tool
    action = mcp_data.action
    payload = mcp_data.payload

    if tool == "dbt":
        if action == "run_model":
            stdout, stderr = run_dbt_model(payload)
            notify_slack(f"✅ dbt model '{payload['model_name']}' run completed.\n\nOutput:\n{stdout}\n\nErrors:\n{stderr}")
        else:
            raise ValueError(f"Unsupported action '{action}' for tool 'dbt'")
    else:
        raise ValueError(f"Unsupported tool '{tool}'")

@app.post("/trigger")
async def trigger_tool(request: Request, mcp_payload: MCPPayload):
    try:
        print(f"[MCP] Request from {mcp_payload.metadata.get('requested_by', 'unknown')} at {datetime.utcnow().isoformat()} UTC")
        handle_mcp_request(mcp_payload)
        return {"status": "success", "message": "MCP executed."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        with open(file_path, "r") as f:
            mcp_data = json.load(f)
        print(f"[MCP] Request received at {datetime.utcnow().isoformat()} UTC")
        handle_mcp_request(MCPPayload(**mcp_data))
    else:
        uvicorn.run("mcp_dispatcher:app", host="0.0.0.0", port=8000, reload=True)
