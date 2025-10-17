import json
import requests
from typing import Dict, Any


def check_task_status(task_id: str, avni_mcp_server_url: str) -> Dict[str, Any]:
    session = requests.Session()

    status_url = f"{avni_mcp_server_url}/process-config-status/{task_id}"

    print(f"🔍 Checking task status: {task_id}")

    try:
        status_response = session.get(status_url, timeout=10)

        if status_response.status_code != 200:
            error_text = status_response.text
            return {
                "error": f"Status check HTTP {status_response.status_code}",
                "message": error_text,
                "task_id": task_id,
            }

        status_result = status_response.json()
        status = status_result.get("status")
        progress = status_result.get("progress", "")

        if progress:
            print(f"📝 Progress: {progress}")

        return status_result

    except requests.exceptions.RequestException as e:
        return {"error": "Status check failed", "message": str(e), "task_id": task_id}


def main(output: Dict[str, Any], avni_mcp_server_url: str):
    print("🚀 Config Task Status Check")
    print("=" * 40)

    task_id = output.get("task_id")
    result = check_task_status(task_id, avni_mcp_server_url)

    status = result.get("status")
    if status in ["completed", "failed", "expired"]:
        print(f"✅ Terminal status reached: {status}")

    print("\n" + "=" * 40)
    print("🏁 FINAL RESULT:")
    print(json.dumps(result, indent=2))

    return {"output": result}
