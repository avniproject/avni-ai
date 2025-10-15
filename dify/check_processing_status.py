import json
import requests
from typing import Dict, Any


def check_task_status(
    task_id: str, staging_url: str = "https://staging-mcp.avniproject.org"
) -> Dict[str, Any]:
    """
    Check task status once.

    Args:
        task_id: Task ID to check
        staging_url: MCP staging server URL

    Returns:
        Task status result
    """
    staging_url = staging_url.rstrip("/")
    session = requests.Session()

    status_url = f"{staging_url}/process-config-status/{task_id}"

    print(f"🔍 Checking task status: {task_id}")

    try:
        status_response = session.get(status_url, timeout=10)

        if status_response.status_code != 200:
            error_text = status_response.text
            print(f"❌ Status check error {status_response.status_code}: {error_text}")
            return {
                "error": f"Status check HTTP {status_response.status_code}",
                "message": error_text,
                "task_id": task_id,
            }

        status_result = status_response.json()
        status = status_result.get("status")
        progress = status_result.get("progress", "")

        print(f"📊 Status = {status}")
        if progress:
            print(f"📝 Progress: {progress}")

        return status_result

    except requests.exceptions.RequestException as e:
        print(f"🔥 Status check request failed: {e}")
        return {"error": "Status check failed", "message": str(e), "task_id": task_id}


def main(submit_output: Dict[str, Any], loop: bool = False):
    """
    Check task status once.

    Args:
        submit_output: Output from submit_async_config.py containing task_id
        loop: Parameter for external loop handling (updates to False if terminal status)
    """
    print("🚀 Avni Async Status Check")
    print("=" * 40)

    # Extract task_id from submit output
    if "output" in submit_output:
        task_id = submit_output["output"].get("task_id")
    elif "submit_output" in submit_output:
        task_id = submit_output["submit_output"].get("task_id")
    else:
        task_id = submit_output.get("task_id")

    if not task_id:
        error_result = {
            "error": "No task_id found in submit output",
            "submit_output": submit_output,
        }
        print("❌ No task_id found in submit output")
        print(json.dumps(error_result, indent=2))
        return {"output": error_result}

    print(f"🎯 Extracted Task ID: {task_id}")

    # Check status once
    staging_url = "https://staging-mcp.avniproject.org"
    result = check_task_status(task_id=task_id, staging_url=staging_url)

    # Update loop variable if terminal status reached
    status = result.get("status")
    if status in ["completed", "failed", "expired"]:
        loop = False
        print(f"✅ Terminal status reached: {status}")

    print("\n" + "=" * 40)
    print("🏁 FINAL RESULT:")
    print(json.dumps(result, indent=2))

    return {"output": result}
