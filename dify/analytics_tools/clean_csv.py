#!/usr/bin/env python3
import csv
import sys

USERS_TO_REMOVE = {
    "Himesh",
    "Himesh R",
    "maha",
    "ombh",
    "jimy",
    "Siddharth",
    "Adam",
    "Dinesh G",
    "Mohammed Taqi Afsar",
    "Subhamita K",
    "Vinay Venu",
    "mahanew4",
    "DInesh G",
    "",
    None,
}

ORGS_TO_REMOVE = {"DifyTest", "copilot"}


def clean_csv(input_file, output_file):
    rows_kept = 0
    rows_removed = 0

    with (
        open(input_file, "r", encoding="utf-8") as infile,
        open(output_file, "w", newline="", encoding="utf-8") as outfile,
    ):
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

        writer.writeheader()

        for row in reader:
            user_name = row.get("user_name", "").strip()
            org_name = row.get("org_name", "").strip()

            if user_name == "":
                user_name = None
            if org_name == "":
                org_name = None

            should_remove = user_name in USERS_TO_REMOVE or org_name in ORGS_TO_REMOVE

            if should_remove:
                rows_removed += 1
                print(f"Removed: user='{user_name}', org='{org_name}'")
            else:
                writer.writerow(row)
                rows_kept += 1

    print(f"\nCleaning completed!")
    print(f"Rows kept: {rows_kept}")
    print(f"Rows removed: {rows_removed}")
    print(f"Output saved to: {output_file}")


if __name__ == "__main__":
    input_file = "messages_20251126_174012.csv"
    output_file = "messages_cleaned.csv"

    try:
        clean_csv(input_file, output_file)
    except FileNotFoundError:
        print(f"Error: Could not find file '{input_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
