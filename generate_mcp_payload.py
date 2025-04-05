def generate_mcp_payload(user_input):
    # Basic NLP processing (could be expanded further)
    if "trigger" in user_input and "model" in user_input:
        model_name = "customer_lifetime_value"
        year = "2024"
        return {
            "mcp_version": "1.0",
            "tool": "dbt",
            "action": "run_model",
            "payload": {
                "project": "analytics_project",
                "model_name": model_name,
                "target_environment": "prod",
                "variables": {
                    "start_date": f"{year}-01-01",
                    "end_date": f"{year}-12-31"
                },
                "flags": {
                    "full_refresh": True,
                    "threads": 2
                }
            },
            "metadata": {
                "requested_by": "Claude",
                "requested_at": datetime.utcnow().isoformat(),
                "description": f"Trigger {model_name} model with full refresh for {year}."
            }
        }
    return {}
