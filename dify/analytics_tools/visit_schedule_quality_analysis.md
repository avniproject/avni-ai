# Avni Visit Scheduling Rule Generation Quality Analysis

- Generated at (UTC): 2026-02-23T11:09:31.160270+00:00
- User scope analyzed: `rules_tester`
- Total conversations: 22
- Valid query conversations: 22

## Data Processing
- Conversations fetched from Dify app API: `GET /conversations`
- Message-level content fetched from Dify app API: `GET /messages`
- Invalid queries removed: blank/very short/affirmation-only queries (`YES`, `OK`, etc.)

## Categorization Summary
- quality_distribution: {'Good response': 14, 'Bad response': 8}
- relevance_distribution: {'Relevant to Avni': 22}
- query_type_distribution: {'Programmatic': 22}
- feasibility_distribution: {'Feasible with Avni/AI Assistant': 22}

## Areas of Concern
- Conversations flagged as bad response: 8
- Primary concern tags: {'missing_final_rule_code': 7, 'missing_scenario_validation': 1}
- Bad-response topic clusters: {'gestational_age_timing_rules': 3, 'nutrition_followup_rules': 2, 'anc_followup_rules': 3}
- Typical failure pattern: scenario table generated but final rule code missing in same conversation flow.

## Recommendations for Improvement
1. Enforce confirmation prompt template and detection robustness in the conversation strategy.
2. Add a guardrail test asserting two-turn completion (`scenario table` -> `YES` -> `final code`) for each rules scenario.
3. Track and alert on one-turn rule-generation conversations as a quality regression signal.
4. Add structured metadata tags (`scenario_table_present`, `confirmation_prompt_present`, `final_code_present`) to simplify monitoring.
5. For poor topics, add focused prompt examples and negative examples to reduce drop-off before code generation.

## Output Files
- Raw conversations: `dify/analytics_tools/rules_tester_conversations_raw.json`
- Classified conversations: `dify/analytics_tools/visit_schedule_query_classification.csv`
- Summary JSON: `dify/analytics_tools/visit_schedule_quality_summary.json`
- Analysis report: `dify/analytics_tools/visit_schedule_quality_analysis.md`