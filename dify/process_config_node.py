import json
import requests
from typing import Dict, Any, Optional


def submit_async_config(
    config: Dict[str, Any],
    avni_auth_token: str,
    avni_base_url: Optional[str] = None,
    staging_url: str = "https://staging-mcp.avniproject.org",
) -> Dict[str, Any]:
    """
    Submit configuration for async processing.

    Args:
        config: Configuration JSON object
        avni_auth_token: Avni authentication token
        avni_base_url: Optional Avni API base URL
        staging_url: MCP staging server URL

    Returns:
        Response with task_id or error
    """
    staging_url = staging_url.rstrip("/")
    session = requests.Session()

    # Submit configuration
    submit_url = f"{staging_url}/process-config-async"

    headers = {"Content-Type": "application/json", "avni-auth-token": avni_auth_token}

    if avni_base_url:
        headers["avni-base-url"] = avni_base_url

    body = {"config": config}

    print(f"📤 Submitting config to: {submit_url}")
    print(f"📋 Headers: {json.dumps(headers, indent=2)}")
    print(f"📦 Body size: {len(json.dumps(body).encode('utf-8'))} bytes")

    try:
        response = session.post(submit_url, headers=headers, json=body, timeout=30)

        print(f"✅ Submit response status: {response.status_code}")

        if response.status_code != 200:
            error_text = response.text
            print(f"❌ Submit error {response.status_code}: {error_text}")
            return {"error": f"HTTP {response.status_code}", "message": error_text}

        result = response.json()
        task_id = result.get("task_id")

        if not task_id:
            return {"error": "No task_id returned", "response": result}

        print(f"🎯 Task ID: {task_id}")
        return {"task_id": task_id, "status": "submitted"}

    except requests.exceptions.RequestException as e:
        print(f"🔥 Submit request failed: {e}")
        return {"error": "Submit request failed", "message": str(e)}


def main(avni_auth_token: str, avni_base_url: str, config: Dict[str, Any]):
    """
    Submit configuration for async processing.

    Args:
        avni_auth_token: Avni authentication token
        avni_base_url: Avni API base URL
        config: Configuration object to process
    """
    print("🚀 Avni Async Config Submission")
    print("=" * 40)

    print("📋 Configuration preview:")
    print(json.dumps(config, indent=2)[:300] + "...")

    # Submit configuration
    staging_url = "https://staging-mcp.avniproject.org"
    result = submit_async_config(
        config=config,
        avni_auth_token=avni_auth_token,
        avni_base_url=avni_base_url,
        staging_url=staging_url,
    )

    print("\n" + "=" * 40)
    print("🏁 SUBMISSION RESULT:")
    print(json.dumps(result, indent=2))

    return {"output": result}
