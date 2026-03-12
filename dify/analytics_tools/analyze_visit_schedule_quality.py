#!/usr/bin/env python3
"""
Analyze Avni visit-schedule assistant conversation quality from Dify app API.

Outputs:
- rules_tester_conversations_raw.json
- visit_schedule_query_classification.csv
- visit_schedule_quality_summary.json
- visit_schedule_quality_analysis.md
"""

import csv
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Dict, List

import requests


AFFIRMATIVES = {
    "yes",
    "y",
    "ok",
    "okay",
    "go ahead",
    "proceed",
    "confirmed",
    "approve",
    "approved",
    "looks good",
    "that works",
    "perfect",
    "sure",
    "yep",
    "yup",
}

AVNI_KEYWORDS = {
    "avni",
    "visit",
    "schedule",
    "encounter",
    "enrolment",
    "program",
    "subject",
    "anc",
    "pnc",
    "growth",
    "nutrition",
    "gestational",
    "follow up",
    "follow-up",
}

TECHNICAL_KEYWORDS = {
    "javascript",
    "js",
    "code",
    "function",
    "uuid",
    "api",
    "builder",
    "imports",
    "rulecondition",
    "visitschedulebuilder",
    "return",
}

INFEASIBLE_PATTERNS = [
    r"not supported",
    r"cannot",
    r"can't",
    r"unable to",
    r"outside scope",
    r"do not have access",
]


def normalize(text: str) -> str:
    text = (text or "").strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def is_valid_query(query: str) -> bool:
    nq = normalize(query)
    if not nq:
        return False
    if nq in AFFIRMATIVES:
        return False
    if len(nq) < 5:
        return False
    return True


def classify_query_type(query: str) -> str:
    nq = normalize(query)
    if any(keyword in nq for keyword in TECHNICAL_KEYWORDS):
        return "Technical"
    return "Programmatic"


def classify_relevance(query: str, request_type: str) -> str:
    nq = normalize(query)
    if request_type == "VisitSchedule":
        return "Relevant to Avni"
    if any(keyword in nq for keyword in AVNI_KEYWORDS):
        return "Relevant to Avni"
    return "Non-relevant"


def has_pattern(text: str, patterns: List[str]) -> bool:
    nt = normalize(text)
    return any(re.search(pattern, nt) for pattern in patterns)


def to_iso(ts: Any) -> str:
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).isoformat()
    except Exception:
        return ""


def get_conversations(base_url: str, headers: Dict[str, str], user: str) -> List[Dict]:
    conversations: List[Dict] = []
    last_id = None
    limit = 100

    while True:
        params = {"user": user, "limit": limit}
        if last_id:
            params["last_id"] = last_id

        response = requests.get(
            f"{base_url}/conversations", headers=headers, params=params, timeout=60
        )
        response.raise_for_status()
        payload = response.json()
        batch = payload.get("data", [])

        if not batch:
            break

        conversations.extend(batch)

        if not payload.get("has_more"):
            break

        last_id = batch[-1]["id"]

    return conversations


def get_messages(
    base_url: str, headers: Dict[str, str], conversation_id: str, user: str
) -> List[Dict]:
    params = {"conversation_id": conversation_id, "user": user, "limit": 100}
    response = requests.get(
        f"{base_url}/messages", headers=headers, params=params, timeout=60
    )
    response.raise_for_status()
    payload = response.json()
    messages = payload.get("data", [])
    messages.sort(key=lambda m: m.get("created_at", 0))
    return messages


def build_records(
    conversations: List[Dict], base_url: str, headers: Dict[str, str], user: str
):
    raw_dump = []
    records = []

    for conv in conversations:
        conversation_id = conv["id"]
        messages = get_messages(base_url, headers, conversation_id, user)

        raw_dump.append({"conversation": conv, "messages": messages})

        request_type = (conv.get("inputs") or {}).get("requestType", "")
        user_queries = [
            m.get("query", "") for m in messages if is_valid_query(m.get("query", ""))
        ]
        initial_query = user_queries[0] if user_queries else ""

        first_answer = messages[0].get("answer", "") if messages else ""
        has_scenarios_table = "| case |" in normalize(
            first_answer
        ) and "| trigger |" in normalize(first_answer)
        has_confirmation_prompt = (
            "do these scenarios match" in normalize(first_answer)
            or "if yes, i’ll generate" in normalize(first_answer)
            or "if yes, i'll generate" in normalize(first_answer)
            or "let me know what to change" in normalize(first_answer)
        )

        has_final_code = any(
            marker in normalize(m.get("answer", ""))
            for m in messages
            for marker in [
                '"use strict"',
                "```javascript",
                "visitschedulebuilder",
                "({ params, imports }) =>",
                "({params, imports}) =>",
            ]
        )

        relevance = classify_relevance(initial_query, request_type)
        query_type = (
            classify_query_type(initial_query) if initial_query else "Programmatic"
        )

        if any(has_pattern(m.get("answer", ""), INFEASIBLE_PATTERNS) for m in messages):
            feasibility = "Not-feasible with Avni/AI Assistant"
        elif has_scenarios_table or has_final_code:
            feasibility = "Feasible with Avni/AI Assistant"
        else:
            feasibility = "Not-feasible with Avni/AI Assistant"

        response_quality = (
            "Good response"
            if has_scenarios_table and has_final_code
            else "Bad response"
        )

        concern_tags = []
        if not has_scenarios_table:
            concern_tags.append("missing_scenario_validation")
        if has_scenarios_table and not has_confirmation_prompt:
            concern_tags.append("missing_confirmation_prompt")
        if not has_final_code:
            concern_tags.append("missing_final_rule_code")
        if not initial_query:
            concern_tags.append("invalid_or_missing_query")

        records.append(
            {
                "conversation_id": conversation_id,
                "conversation_name": conv.get("name", ""),
                "created_at": conv.get("created_at", ""),
                "created_at_iso_utc": to_iso(conv.get("created_at")),
                "request_type": request_type,
                "initial_query": initial_query,
                "turn_count": len(messages),
                "valid_query_count": len(user_queries),
                "has_scenarios_table": has_scenarios_table,
                "has_confirmation_prompt": has_confirmation_prompt,
                "has_final_rule_code": has_final_code,
                "response_quality": response_quality,
                "relevance": relevance,
                "query_type": query_type,
                "feasibility": feasibility,
                "concern_tags": ";".join(concern_tags),
            }
        )

    return raw_dump, records


def build_summary(records: List[Dict]) -> Dict[str, Any]:
    summary: Dict[str, Any] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_conversations": len(records),
        "valid_query_conversations": sum(1 for r in records if r["initial_query"]),
        "quality_distribution": dict(Counter(r["response_quality"] for r in records)),
        "relevance_distribution": dict(Counter(r["relevance"] for r in records)),
        "query_type_distribution": dict(Counter(r["query_type"] for r in records)),
        "feasibility_distribution": dict(Counter(r["feasibility"] for r in records)),
        "concern_tag_distribution": dict(
            Counter(
                tag
                for r in records
                for tag in (r["concern_tags"].split(";") if r["concern_tags"] else [])
            )
        ),
    }

    bad_records = [r for r in records if r["response_quality"] == "Bad response"]
    bad_topic_counter = Counter()
    for record in bad_records:
        nq = normalize(record["initial_query"])
        if not nq:
            bad_topic_counter["missing_query"] += 1
        elif "nutritional status" in nq or "sam" in nq or "mam" in nq:
            bad_topic_counter["nutrition_followup_rules"] += 1
        elif "gestational age" in nq or "20 weeks" in nq or "28 weeks" in nq:
            bad_topic_counter["gestational_age_timing_rules"] += 1
        elif "anc" in nq:
            bad_topic_counter["anc_followup_rules"] += 1
        else:
            bad_topic_counter["other"] += 1

    summary["top_bad_topics"] = dict(bad_topic_counter)
    return summary


def write_outputs(
    out_dir: str,
    user: str,
    raw_dump: List[Dict],
    records: List[Dict],
    summary: Dict[str, Any],
) -> Dict[str, str]:
    raw_path = os.path.join(out_dir, "rules_tester_conversations_raw.json")
    csv_path = os.path.join(out_dir, "visit_schedule_query_classification.csv")
    summary_path = os.path.join(out_dir, "visit_schedule_quality_summary.json")
    report_path = os.path.join(out_dir, "visit_schedule_quality_analysis.md")

    with open(raw_path, "w", encoding="utf-8") as file:
        json.dump(raw_dump, file, indent=2, ensure_ascii=False)

    if records:
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)

    with open(summary_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    lines = [
        "# Avni Visit Scheduling Rule Generation Quality Analysis",
        "",
        f"- Generated at (UTC): {summary['generated_at_utc']}",
        f"- User scope analyzed: `{user}`",
        f"- Total conversations: {summary['total_conversations']}",
        f"- Valid query conversations: {summary['valid_query_conversations']}",
        "",
        "## Data Processing",
        "- Conversations fetched from Dify app API: `GET /conversations`",
        "- Message-level content fetched from Dify app API: `GET /messages`",
        "- Invalid queries removed: blank/very short/affirmation-only queries (`YES`, `OK`, etc.)",
        "",
        "## Categorization Summary",
        f"- quality_distribution: {summary.get('quality_distribution', {})}",
        f"- relevance_distribution: {summary.get('relevance_distribution', {})}",
        f"- query_type_distribution: {summary.get('query_type_distribution', {})}",
        f"- feasibility_distribution: {summary.get('feasibility_distribution', {})}",
        "",
        "## Areas of Concern",
    ]

    bad_count = summary.get("quality_distribution", {}).get("Bad response", 0)
    if bad_count:
        lines.extend(
            [
                f"- Conversations flagged as bad response: {bad_count}",
                f"- Primary concern tags: {summary.get('concern_tag_distribution', {})}",
                f"- Bad-response topic clusters: {summary.get('top_bad_topics', {})}",
                "- Typical failure pattern: scenario table generated but final rule code missing in same conversation flow.",
            ]
        )
    else:
        lines.append("- No bad-response conversations detected in this dataset.")

    lines.extend(
        [
            "",
            "## Recommendations for Improvement",
            "1. Enforce confirmation prompt template and detection robustness in the conversation strategy.",
            "2. Add a guardrail test asserting two-turn completion (`scenario table` -> `YES` -> `final code`) for each rules scenario.",
            "3. Track and alert on one-turn rule-generation conversations as a quality regression signal.",
            "4. Add structured metadata tags (`scenario_table_present`, `confirmation_prompt_present`, `final_code_present`) to simplify monitoring.",
            "5. For poor topics, add focused prompt examples and negative examples to reduce drop-off before code generation.",
            "",
            "## Output Files",
            f"- Raw conversations: `{raw_path}`",
            f"- Classified conversations: `{csv_path}`",
            f"- Summary JSON: `{summary_path}`",
            f"- Analysis report: `{report_path}`",
        ]
    )

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    return {
        "raw": raw_path,
        "classified_csv": csv_path,
        "summary_json": summary_path,
        "report_md": report_path,
    }


def main():
    base_url = os.getenv("DIFY_API_BASE_URL", "https://api.dify.ai/v1").rstrip("/")
    api_key = os.getenv("DIFY_API_KEY", "")
    user = os.getenv("DIFY_ANALYSIS_USER", "rules_tester")
    out_dir = os.getenv("DIFY_ANALYSIS_OUT_DIR", "dify/analytics_tools")
    os.makedirs(out_dir, exist_ok=True)

    if not api_key:
        raise SystemExit("DIFY_API_KEY is missing.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    conversations = get_conversations(base_url, headers, user)
    raw_dump, records = build_records(conversations, base_url, headers, user)
    summary = build_summary(records)
    files = write_outputs(out_dir, user, raw_dump, records, summary)

    result = {
        "user_scope": user,
        "total_conversations": summary["total_conversations"],
        "valid_query_conversations": summary["valid_query_conversations"],
        "quality_distribution": summary["quality_distribution"],
        "relevance_distribution": summary["relevance_distribution"],
        "query_type_distribution": summary["query_type_distribution"],
        "feasibility_distribution": summary["feasibility_distribution"],
        "concern_tag_distribution": summary["concern_tag_distribution"],
        "top_bad_topics": summary["top_bad_topics"],
        "files": files,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
