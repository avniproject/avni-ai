#!/usr/bin/env python3
"""
Consolidated Form Validation Analysis Tool
Combines all form analysis capabilities with different modes:
- full: Analyze all forms in reference bundles
- quick: Sample-based analysis for rapid insights
- new-only: Analyze only new organizations
"""

import os
import json
import re
import random
import argparse
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple
from collections import defaultdict


def find_organizations(reference_dir: Path, exclude_new: bool = False) -> List[Path]:
    """Find organizations in reference directory"""
    organizations = [d for d in reference_dir.iterdir() if d.is_dir()]

    if exclude_new:
        # Keep only APF (original) for full analysis
        organizations = [org for org in organizations if org.name == "apf"]
    else:
        # Exclude APF for new-only analysis
        organizations = [org for org in organizations if org.name != "apf"]

    return organizations


def find_form_files(directory: Path) -> List[Path]:
    """Find all form files in the directory"""
    form_files = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".") and d not in ["translations", "extensions"]
        ]

        for file in files:
            if file.endswith((".js", ".json")) and not file.startswith("."):
                file_path = Path(root) / file
                form_files.append(file_path)

    return form_files


def parse_form_file_lightweight(file_path: Path) -> Dict[str, Any]:
    """Lightweight form parsing - extract only concept types and basic info"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Quick extraction of dataType patterns
        data_types = set()
        data_type_matches = re.findall(r'"dataType"\s*:\s*"([^"]+)"', content)
        data_types.update(data_type_matches)

        # Extract basic form info
        name_match = re.search(r'"name"\s*:\s*"([^"]+)"', content)
        form_type_match = re.search(r'"formType"\s*:\s*"([^"]+)"', content)

        return {
            "file": str(file_path),
            "name": name_match.group(1) if name_match else "Unknown",
            "formType": form_type_match.group(1) if form_type_match else "Unknown",
            "dataTypes": list(data_types),
            "file_size": file_path.stat().st_size,
        }

    except Exception as e:
        print(f"⚠️  Could not parse {file_path}: {e}")
        return {}


def get_sample_forms(organization_dir: Path, sample_size: int = 8) -> List[Path]:
    """Get a representative sample of forms from an organization"""
    forms_dir = organization_dir / "forms"
    if not forms_dir.exists():
        return []

    all_forms = []
    for file in forms_dir.glob("*.js"):
        all_forms.append(file)
    for file in forms_dir.glob("*.json"):
        all_forms.append(file)

    if not all_forms:
        return []

    if len(all_forms) <= sample_size:
        return all_forms

    # Sample diverse forms by size
    sorted_forms = sorted(all_forms, key=lambda f: f.stat().st_size)

    # Take samples from different size ranges
    samples = []
    size_ranges = [
        (0, len(sorted_forms) // 4),
        (len(sorted_forms) // 4, len(sorted_forms) // 2),
        (len(sorted_forms) // 2, 3 * len(sorted_forms) // 4),
        (3 * len(sorted_forms) // 4, len(sorted_forms)),
    ]

    for start, end in size_ranges:
        if sorted_forms[start:end]:
            samples.append(random.choice(sorted_forms[start:end]))

    remaining = [f for f in all_forms if f not in samples]
    samples.extend(
        random.sample(remaining, min(sample_size - len(samples), len(remaining)))
    )

    return samples[:sample_size]


def analyze_form_elements(elements: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze form elements to identify patterns"""

    concept_types = set()
    form_types = set()
    data_type_combinations = set()
    field_names = []

    for element in elements:
        concept = element.get("concept", {})
        data_type = concept.get("dataType", "Unknown")
        element_type = element.get("type", "Unknown")
        field_name = element.get("name", "Unknown")
        form_type = element.get("_form_type", "Unknown")

        concept_types.add(data_type)
        form_types.add(form_type)
        data_type_combinations.add(f"{data_type}_{element_type}")
        field_names.append(field_name.lower())

    known_concept_types = {
        "Date",
        "DateTime",
        "Text",
        "Notes",
        "Numeric",
        "SingleSelect",
        "MultiSelect",
        "Image",
        "Video",
        "Audio",
        "File",
        "Coded",
        "QuestionGroup",
        "PhoneNumber",
        "Location",
        "Subject",
        "GroupAffiliation",
        "Encounter",
        "NA",
        "Time",
        "Duration",
        "Id",
        "ImageV2",
    }

    new_concept_types = concept_types - known_concept_types

    return {
        "total_elements": len(elements),
        "concept_types_found": sorted(list(concept_types)),
        "form_types_found": sorted(list(form_types)),
        "data_type_combinations": sorted(list(data_type_combinations)),
        "new_concept_types": sorted(list(new_concept_types)),
        "field_name_patterns": analyze_field_name_patterns(field_names),
    }


def analyze_field_name_patterns(field_names: List[str]) -> Dict[str, Any]:
    """Analyze field names to identify validation patterns"""

    categories = {
        "assessment": ["assessment", "score", "grade", "evaluation", "performance"],
        "capacity_building": ["training", "capacity", "skill", "workshop", "session"],
        "monitoring": ["monitoring", "observation", "inspection", "review", "audit"],
        "logistics": ["distribution", "dispatch", "inventory", "stock", "supply"],
        "infrastructure": [
            "building",
            "facility",
            "infrastructure",
            "space",
            "equipment",
        ],
        "administrative": [
            "registration",
            "approval",
            "verification",
            "certification",
            "authorization",
        ],
    }

    categorized_fields = defaultdict(list)
    uncategorized = []

    for field_name in field_names:
        categorized = False
        for category, keywords in categories.items():
            if any(keyword in field_name for keyword in keywords):
                categorized_fields[category].append(field_name)
                categorized = True
                break
        if not categorized:
            uncategorized.append(field_name)

    return {
        "categorized_fields": {
            cat: fields[:5] for cat, fields in categorized_fields.items()
        },
        "uncategorized_sample": uncategorized[:10],
        "total_categorized": sum(len(fields) for fields in categorized_fields.values()),
        "total_uncategorized": len(uncategorized),
    }


def analyze_sampled_forms(sampled_forms: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze sampled forms to identify new patterns"""

    all_data_types = set()
    form_types = set()
    domain_keywords = defaultdict(set)

    domain_patterns = {
        "education": [
            "school",
            "anganwadi",
            "teacher",
            "student",
            "assessment",
            "capacity",
            "training",
        ],
        "logistics": [
            "distribution",
            "dispatch",
            "inventory",
            "stock",
            "supply",
            "village",
        ],
        "health": ["health", "medical", "patient", "treatment", "screening"],
        "monitoring": ["monitoring", "observation", "review", "audit", "inspection"],
        "administrative": ["registration", "approval", "verification", "certification"],
    }

    for form_info in sampled_forms:
        all_data_types.update(form_info.get("dataTypes", []))
        form_types.add(form_info.get("formType", "Unknown"))

        form_name = form_info.get("name", "").lower()
        for domain, keywords in domain_patterns.items():
            if any(keyword in form_name for keyword in keywords):
                domain_keywords[domain].update(form_info.get("dataTypes", []))

    known_concept_types = {
        "Date",
        "DateTime",
        "Text",
        "Notes",
        "Numeric",
        "SingleSelect",
        "MultiSelect",
        "Image",
        "Video",
        "Audio",
        "File",
        "Coded",
        "QuestionGroup",
        "PhoneNumber",
        "Location",
        "Subject",
        "GroupAffiliation",
        "Encounter",
        "NA",
        "Time",
        "Duration",
        "Id",
        "ImageV2",
    }

    new_concept_types = all_data_types - known_concept_types

    return {
        "total_forms_sampled": len(sampled_forms),
        "data_types_found": sorted(list(all_data_types)),
        "form_types_found": sorted(list(form_types)),
        "new_concept_types": sorted(list(new_concept_types)),
        "domain_patterns": {
            domain: sorted(list(patterns))
            for domain, patterns in domain_keywords.items()
        },
        "sampled_forms_info": sampled_forms[:5],
    }


def run_full_analysis():
    """Run comprehensive analysis of all forms"""
    print("🔍 Running Full Form Analysis")
    print("=" * 40)

    reference_dir = Path("/Users/himeshr/IdeaProjects/avni-impl-bundles/reference")
    organizations = find_organizations(reference_dir, exclude_new=True)

    if not organizations:
        print("❌ No organizations found for full analysis")
        return

    print(f"📁 Analyzing {len(organizations)} organization(s)")

    all_elements = []
    for org_dir in organizations:
        print(f"🔍 Processing {org_dir.name}...")

        form_files = find_form_files(org_dir)
        print(f"   Found {len(form_files)} form files")

        for form_file in form_files:
            form_info = parse_form_file_lightweight(form_file)
            if form_info:
                all_elements.append(form_info)

    analysis = analyze_form_elements(all_elements)

    print(f"\n📊 Full Analysis Results:")
    print(f"   Total forms processed: {len(all_elements)}")
    print(f"   Concept types found: {len(analysis['concept_types_found'])}")
    print(f"   Form types found: {len(analysis['form_types_found'])}")

    if analysis["new_concept_types"]:
        print(f"   New concept types: {', '.join(analysis['new_concept_types'])}")

    return analysis


def run_quick_analysis():
    """Run quick sampling analysis"""
    print("🚀 Running Quick Form Analysis")
    print("=" * 40)

    reference_dir = Path("/Users/himeshr/IdeaProjects/avni-impl-bundles/reference")
    organizations = find_organizations(reference_dir, exclude_new=False)

    if not organizations:
        print("❌ No new organizations found")
        return

    print(f"📁 Analyzing {len(organizations)} new organizations")

    all_sampled_forms = []

    for org_dir in organizations:
        print(f"🔍 Sampling forms from {org_dir.name}...")

        sample_forms = get_sample_forms(org_dir, sample_size=6)
        print(f"   Selected {len(sample_forms)} forms")

        for form_file in sample_forms:
            form_info = parse_form_file_lightweight(form_file)
            if form_info:
                all_sampled_forms.append(form_info)

    analysis = analyze_sampled_forms(all_sampled_forms)

    print(f"\n📊 Quick Analysis Results:")
    print(f"   Total forms sampled: {len(all_sampled_forms)}")
    print(f"   Concept types found: {len(analysis['data_types_found'])}")
    print(f"   New concept types: {len(analysis['new_concept_types'])}")

    if analysis["new_concept_types"]:
        print(f"   🔍 New types: {', '.join(analysis['new_concept_types'])}")

    return analysis


def run_new_only_analysis():
    """Run analysis focusing only on new organizations"""
    print("🆕 Running New Organizations Analysis")
    print("=" * 40)

    reference_dir = Path("/Users/himeshr/IdeaProjects/avni-impl-bundles/reference")
    organizations = find_organizations(reference_dir, exclude_new=False)

    if not organizations:
        print("❌ No new organizations found")
        return

    print(f"📁 Analyzing {len(organizations)} new organizations:")
    for org in organizations:
        print(f"   - {org.name}")

    all_sampled_forms = []

    for org_dir in organizations:
        print(f"\n🔍 Analyzing {org_dir.name}...")

        sample_forms = get_sample_forms(org_dir, sample_size=6)
        org_form_info = []

        for form_file in sample_forms:
            form_info = parse_form_file_lightweight(form_file)
            if form_info:
                org_form_info.append(form_info)

        all_sampled_forms.extend(org_form_info)
        print(f"   Processed {len(org_form_info)} forms")

    analysis = analyze_sampled_forms(all_sampled_forms)

    print(f"\n📊 New Organizations Analysis Results:")
    print(f"   Organizations analyzed: {len(organizations)}")
    print(f"   Total forms sampled: {len(all_sampled_forms)}")
    print(f"   Concept types found: {len(analysis['data_types_found'])}")
    print(f"   Form types found: {len(analysis['form_types_found'])}")
    print(f"   New concept types: {len(analysis['new_concept_types'])}")

    if analysis["new_concept_types"]:
        print(f"   🔍 NEW TYPES: {', '.join(analysis['new_concept_types'])}")

    print(f"\n📋 Domain Patterns:")
    for domain, patterns in analysis["domain_patterns"].items():
        if patterns:
            print(f"   {domain.title()}: {len(patterns)} patterns")

    return analysis


def main():
    """Main entry point for consolidated form validation analysis"""
    parser = argparse.ArgumentParser(description="Form Validation Analysis Tool")
    parser.add_argument(
        "mode",
        choices=["full", "quick", "new-only"],
        help="Analysis mode: full (all forms), quick (sampling), new-only (new organizations only)",
    )

    args = parser.parse_args()

    print("🧪 Form Validation Analysis Tool")
    print("=" * 50)

    # Run analysis based on mode
    if args.mode == "full":
        analysis = run_full_analysis()
        filename = "full_form_analysis.json"
    elif args.mode == "quick":
        analysis = run_quick_analysis()
        filename = "quick_form_analysis.json"
    elif args.mode == "new-only":
        analysis = run_new_only_analysis()
        filename = "new_organizations_analysis.json"

    # Save results
    if analysis:
        output_dir = Path("/Users/himeshr/IdeaProjects/avni-ai/docs/form_validation")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / filename
        with open(output_file, "w") as f:
            json.dump(analysis, f, indent=2)

        print(f"\n✅ Analysis saved to: {output_file}")
    else:
        print("\n❌ Analysis failed")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
