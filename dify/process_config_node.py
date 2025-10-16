import json
import requests
from typing import Dict, Any


def submit_async_config(
    config: Dict[str, Any],
    avni_auth_token: str,
    avni_mcp_server_url: str,
) -> Dict[str, Any]:
    session = requests.Session()

    submit_url = f"{avni_mcp_server_url}/process-config-async"

    headers = {"Content-Type": "application/json", "avni-auth-token": avni_auth_token}

    body = {"config": config}

    print(f"📤 Submitting config to: {submit_url}")
    print(f"📋 Headers: {json.dumps(headers, indent=2)}")
    print(f"📦 Body size: {len(json.dumps(body).encode('utf-8'))} bytes")

    try:
        response = session.post(submit_url, headers=headers, json=body, timeout=30)

        if response.status_code != 200:
            error_text = response.text
            return {"error": f"HTTP {response.status_code}", "message": error_text}

        result = response.json()
        task_id = result.get("task_id")

        if not task_id:
            return {"error": "No task_id returned", "response": result}

        return {"task_id": task_id, "status": "submitted"}

    except requests.exceptions.RequestException as e:
        print(f"🔥 Submit request failed: {e}")
        return {"error": "Submit request failed", "message": str(e)}


def main(avni_auth_token: str, avni_mcp_server_url: str, config: Dict[str, Any]):
    print("🚀 Avni Async Config Submission")
    print("=" * 40)

    print("📋 Configuration preview:")
    print(json.dumps(config, indent=2)[:300] + "...")

    result = submit_async_config(
        config=config,
        avni_auth_token=avni_auth_token,
        avni_mcp_server_url=avni_mcp_server_url,
    )

    print("\n" + "=" * 40)
    print("🏁 SUBMISSION RESULT:")
    print(json.dumps(result, indent=2))

    return {"output": result}
