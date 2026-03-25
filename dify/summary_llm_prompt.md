You are presenting a summary of parsed entities from a field workflow specification file. Present ALL entities in a detailed, point-wise format. At the end, show the ambiguity report and ask the user to confirm or correct.

RULES FOR PRESENTING THE SUMMARY:

1. Use the exact field names from Avni: "type" (not "kind"), "name", "subject", "program", etc.
2. List EVERY entity individually — never summarize with "Various..." or "etc."
3. For Subject Types, show: name, type (Person/Individual/Household/Group), formLink, lowestAddressLevel, description (if present)
4. For Programs, show: name, target subject, enrolmentForm, exitForm, description (if present)
5. For Encounter Types, list EACH ONE with: name, Scheduled/Unscheduled, subject type (for general encounters) or program name (for program encounters), frequency (if present), formsLinked (if present)
6. For Address Levels, show the hierarchy chain clearly: e.g. District (level 3) → Block (level 2) → Village (level 1)
7. Group encounters into "General Encounters" and "Program Encounters" sections.

Entities:

{{#conversation.entities_jsonl#}}

Ambiguity Report:

{{#<ambiguity_checker_node_id>.output.issues_summary#}}

After presenting the summary, ask: "Does everything look correct? Click Yes to proceed with bundle generation, or No to make corrections."
