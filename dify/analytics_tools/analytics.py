#!/usr/bin/env python3

import pandas as pd
from datetime import datetime
import csv


def analyze_real_data(csv_file: str = "messages_cleaned.csv"):
    df = pd.read_csv(csv_file)
    df["created_at"] = pd.to_datetime(df["created_at"], unit="s")
    df["date"] = df["created_at"].dt.date
    df["hour"] = df["created_at"].dt.hour
    df["day_of_week"] = df["created_at"].dt.day_name()

    date_range = (df["created_at"].max() - df["created_at"].min()).days + 1

    env_counts = df["org_type"].value_counts()
    org_counts = df["org_name"].value_counts().head(10)
    user_counts = df["user_name"].value_counts().head(10)
    hourly_counts = df["hour"].value_counts().sort_index()
    daily_counts = df["day_of_week"].value_counts()
    conv_lengths = df.groupby("conversation_id").size()
    query_lengths = df["query"].fillna("").str.len()
    answer_lengths = df["answer"].fillna("").str.len()
    response_times = df["provider_response_latency"].fillna(0)
    prompt_tokens = df["prompt_tokens"].fillna(0).sum()
    completion_tokens = df["completion_tokens"].fillna(0).sum()
    total_tokens = df["total_tokens"].fillna(0).sum()
    total_cost = df["total_price"].fillna(0).sum()
    avg_cost_per_message = df["total_price"].fillna(0).mean()
    cost_by_env = (
        df.groupby("org_type")["total_price"].sum().sort_values(ascending=False)
    )
    duplicate_queries = df["query"].value_counts()
    exact_duplicates = duplicate_queries[duplicate_queries > 1].head(5)

    return {
        "summary": {
            "total_messages": len(df),
            "total_conversations": df["conversation_id"].nunique(),
            "unique_users": df["user_name"].nunique(),
            "unique_organizations": df["org_name"].nunique(),
            "date_range_days": date_range,
            "messages_per_day": len(df) / date_range,
        },
        "environment_distribution": env_counts.to_dict(),
        "top_organizations": org_counts.head(10).to_dict(),
        "top_users": user_counts.head(10).to_dict(),
        "hourly_distribution": hourly_counts.to_dict(),
        "daily_distribution": daily_counts.to_dict(),
        "conversation_stats": {
            "avg_length": float(conv_lengths.mean()),
            "median_length": float(conv_lengths.median()),
            "max_length": int(conv_lengths.max()),
            "single_message_convs": int((conv_lengths == 1).sum()),
        },
        "text_stats": {
            "avg_query_length": float(query_lengths.mean()),
            "avg_answer_length": float(answer_lengths.mean()),
            "max_query_length": int(query_lengths.max()),
            "max_answer_length": int(answer_lengths.max()),
        },
        "performance_stats": {
            "avg_response_time": float(response_times.mean()),
            "median_response_time": float(response_times.median()),
            "min_response_time": float(response_times.min()),
            "max_response_time": float(response_times.max()),
        },
        "token_stats": {
            "total_prompt_tokens": int(prompt_tokens),
            "total_completion_tokens": int(completion_tokens),
            "total_tokens": int(total_tokens),
            "avg_tokens_per_message": float(total_tokens / len(df)),
        },
        "cost_stats": {
            "total_cost": float(total_cost),
            "avg_cost_per_message": float(avg_cost_per_message),
            "cost_by_environment": cost_by_env.to_dict(),
        },
        "exact_duplicates": exact_duplicates.to_dict()
        if len(exact_duplicates) > 0
        else {},
    }


def export_factual_report_csv(data: dict, output_file: str = None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if output_file is None:
        output_file = f"complete_analytics_{timestamp}.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["SUMMARY METRICS", "", ""])
        writer.writerow(["metric", "value", "description"])
        for key, value in data["summary"].items():
            writer.writerow([key, value, f"Overall {key.replace('_', ' ')}"])
        writer.writerow(["", "", ""])
        writer.writerow(["", "", ""])

        writer.writerow(["ENVIRONMENT DISTRIBUTION", "", ""])
        writer.writerow(["environment", "message_count", "percentage"])
        total_messages = sum(data["environment_distribution"].values())
        for env, count in data["environment_distribution"].items():
            percentage = (count / total_messages) * 100
            writer.writerow([env, count, f"{percentage:.1f}%"])
        writer.writerow(["", "", ""])
        writer.writerow(["", "", ""])

        writer.writerow(["TOP 10 ORGANIZATIONS", ""])
        writer.writerow(["organization", "message_count"])
        for org, count in data["top_organizations"].items():
            writer.writerow([org, count])
        writer.writerow(["", ""])
        writer.writerow(["", ""])

        writer.writerow(["TOP 10 USERS", ""])
        writer.writerow(["user_name", "message_count"])
        for user, count in data["top_users"].items():
            writer.writerow([user, count])
        writer.writerow(["", ""])
        writer.writerow(["", ""])

        writer.writerow(["HOURLY USAGE PATTERNS", ""])
        writer.writerow(["hour", "message_count"])
        for hour in sorted(data["hourly_distribution"].keys()):
            count = data["hourly_distribution"][hour]
            writer.writerow([f"{hour:02d}:00", count])
        writer.writerow(["", ""])
        writer.writerow(["", ""])

        writer.writerow(["DAILY USAGE PATTERNS", ""])
        writer.writerow(["day_of_week", "message_count"])
        day_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        for day in day_order:
            count = data["daily_distribution"].get(day, 0)
            writer.writerow([day, count])
        writer.writerow(["", ""])
        writer.writerow(["", ""])

        writer.writerow(["CONVERSATION ANALYSIS", "", ""])
        writer.writerow(["metric", "value", "description"])
        for key, value in data["conversation_stats"].items():
            writer.writerow([key, value, f"Conversation {key.replace('_', ' ')}"])
        writer.writerow(["", "", ""])
        writer.writerow(["", "", ""])

        writer.writerow(["TEXT ANALYSIS", "", ""])
        writer.writerow(["metric", "value", "unit"])
        for key, value in data["text_stats"].items():
            writer.writerow([key, value, "characters"])
        writer.writerow(["", "", ""])
        writer.writerow(["", "", ""])

        writer.writerow(["PERFORMANCE METRICS", "", ""])
        writer.writerow(["metric", "value", "unit"])
        for key, value in data["performance_stats"].items():
            writer.writerow([key, f"{value:.2f}", "seconds"])
        writer.writerow(["", "", ""])
        writer.writerow(["", "", ""])

        writer.writerow(["TOKEN USAGE", "", ""])
        writer.writerow(["metric", "value", "unit"])
        for key, value in data["token_stats"].items():
            unit = "tokens" if "tokens" in key else "tokens_per_message"
            writer.writerow([key, value, unit])
        writer.writerow(["", "", ""])
        writer.writerow(["", "", ""])

        writer.writerow(["COST ANALYSIS", "", ""])
        writer.writerow(["metric", "value", "unit"])
        for key, value in data["cost_stats"].items():
            if key != "cost_by_environment":
                writer.writerow([key, f"{value:.6f}", "USD"])
        writer.writerow(["", "", ""])
        writer.writerow(["", "", ""])

        writer.writerow(["COST BY ENVIRONMENT", "", ""])
        writer.writerow(["environment", "total_cost", "unit"])
        for env, cost in data["cost_stats"]["cost_by_environment"].items():
            writer.writerow([env, f"{cost:.6f}", "USD"])
        writer.writerow(["", "", ""])
        writer.writerow(["", "", ""])

        if data["exact_duplicates"]:
            writer.writerow(["DUPLICATE QUERIES", ""])
            writer.writerow(["query", "frequency"])
            for query, frequency in data["exact_duplicates"].items():
                writer.writerow([query, frequency])

    return output_file


if __name__ == "__main__":
    data = analyze_real_data()
    csv_file = export_factual_report_csv(data)
