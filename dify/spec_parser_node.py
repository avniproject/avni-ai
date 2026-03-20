import requests

def main(file_info: list, existing_entities_jsonl: str, avni_mcp_server_url: str):
    file_url = ""
    if file_info and len(file_info) > 0:
        first_file = file_info[0]
        if isinstance(first_file, dict):
            file_url = first_file.get("url", "") or first_file.get("remote_url", "")
        elif isinstance(first_file, str):
            file_url = first_file

    if not file_url:
        return {"output": {
            "entities_jsonl": [],
            "summary": "Error: No file URL found in uploaded files",
            "ambiguity_report": {},
        }}

    try:
        url = f"{avni_mcp_server_url}/parse-and-validate"
        body = {
            "file_url": file_url,
            "existing_entities_jsonl": existing_entities_jsonl or "",
        }

        print(f"Calling {url} with file URL: {file_url[:80]}...")
        response = requests.post(url, json=body, timeout=60)
        response.raise_for_status()
        result = response.json()

        return {"output": result}

    except Exception as e:
        print(f"Error: {e}")
        return {"output": {
            "entities_jsonl": [],
            "summary": f"Error: {e}",
            "ambiguity_report": {},
        }}
