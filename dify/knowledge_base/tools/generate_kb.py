#!/usr/bin/env python3
"""
Avni AI Assistant Knowledge Base Generator

Reads file_manifest.json and generates markdown files from source content.
Handles three content types:
  - extract: Pull content from known line ranges
  - synthesize: Combine multiple sources + filtered Q&A pairs
  - skeleton: Generate TODO placeholder structure
  - readme: Auto-generate section navigation pages

Usage:
  python3 generate_kb.py                          # Generate all files
  python3 generate_kb.py --section 02             # Generate one section
  python3 generate_kb.py --skip-existing           # Don't overwrite existing files
  python3 generate_kb.py --validate                # Run validation after generation
  python3 generate_kb.py --dry-run                 # Print plan without writing
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime

import yaml


# ---------------------------------------------------------------------------
# SourceLoader
# ---------------------------------------------------------------------------
class SourceLoader:
    """Loads and caches source file contents."""

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self._cache = {}
        self.source_map = {
            "merged.md": os.path.join(base_dir, "merged.md"),
            "README_original.md": os.path.join(
                base_dir, "_archive", "README_original.md"
            ),
            "test-prompts.md": os.path.join(base_dir, "test-prompts.md"),
            "case-studies-faqs.md": os.path.join(base_dir, "case-studies-faqs.md"),
        }

    def _load_file(self, source_key):
        if source_key not in self._cache:
            path = self.source_map.get(source_key)
            if not path or not os.path.exists(path):
                print(f"  WARNING: Source file not found: {source_key} ({path})")
                self._cache[source_key] = []
                return
            with open(path, "r", encoding="utf-8") as f:
                self._cache[source_key] = f.readlines()
        return self._cache[source_key]

    def get_lines(self, source_key, start_line, end_line):
        """Return lines[start_line-1:end_line] (1-indexed, inclusive)."""
        lines = self._load_file(source_key)
        if not lines:
            return ""
        # Convert 1-indexed to 0-indexed
        start = max(0, start_line - 1)
        end = min(len(lines), end_line)
        return "".join(lines[start:end])

    def get_all_qa_pairs(self):
        """Parse test-prompts.md into (question, answer) tuples."""
        lines = self._load_file("test-prompts.md")
        if not lines:
            return []

        pairs = []
        current_q = None
        current_a_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("## "):
                # Save previous pair
                if current_q:
                    answer = "".join(current_a_lines).strip()
                    if answer:
                        pairs.append((current_q, answer))
                current_q = stripped[3:].strip()
                current_a_lines = []
            elif stripped == "# File:":
                # Separator, ignore
                continue
            else:
                if current_q:
                    current_a_lines.append(line)

        # Save last pair
        if current_q:
            answer = "".join(current_a_lines).strip()
            if answer:
                pairs.append((current_q, answer))

        return pairs

    def get_filtered_qa_pairs(self, keywords):
        """Get Q&A pairs filtered by keywords (case-insensitive match in question or answer)."""
        all_pairs = self.get_all_qa_pairs()
        if not keywords:
            return all_pairs

        filtered = []
        for q, a in all_pairs:
            combined = (q + " " + a).lower()
            if any(kw.lower() in combined for kw in keywords):
                filtered.append((q, a))
        return filtered


# ---------------------------------------------------------------------------
# ContentCleaner
# ---------------------------------------------------------------------------
class ContentCleaner:
    """Cleans raw source content for output."""

    def clean(self, text):
        text = self._remove_file_headers(text)
        text = self._remove_bare_yaml(text)
        text = self._clean_html_components(text)
        text = self._fix_escaped_underscores(text)
        text = self._fix_doc_links(text)
        text = self._normalize_headings(text)
        text = self._clean_blank_lines(text)
        return text.strip()

    def _remove_file_headers(self, text):
        """Remove '# File: ...' lines."""
        return re.sub(r"^# File:.*$\n?", "", text, flags=re.MULTILINE)

    def _remove_bare_yaml(self, text):
        """Remove bare YAML metadata lines at the start of extracted content.

        These look like:
            title: Some Title
            excerpt: Some text
              - type: basic
                slug: something
            ---
        """
        lines = text.split("\n")
        content_start = 0
        in_yaml = True

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not in_yaml:
                break

            # Empty lines at the start
            if not stripped:
                content_start = i + 1
                continue

            # YAML-like lines
            if (
                stripped.startswith("title:")
                or stripped.startswith("excerpt:")
                or stripped.startswith("templateKey:")
                or stripped.startswith("date:")
                or stripped.startswith("description:")
                or stripped.startswith("tags:")
                or stripped.startswith("- type:")
                or stripped.startswith("slug:")
                or re.match(r"^\s+-\s+\w+", stripped)  # indented YAML list items
                or stripped == "---"
            ):
                content_start = i + 1
                continue

            # Indented YAML continuation
            if (
                line.startswith("  ")
                and not stripped.startswith("#")
                and not stripped.startswith("*")
            ):
                content_start = i + 1
                continue

            # Found real content
            in_yaml = False
            break

        return "\n".join(lines[content_start:])

    def _clean_html_components(self, text):
        """Convert HTML components to markdown."""
        # <Image> tags -> markdown image
        text = re.sub(
            r'<Image\s+[^>]*src="([^"]*)"[^>]*>\s*(.*?)\s*</Image>',
            r"![\2](\1)",
            text,
            flags=re.DOTALL,
        )
        # Self-closing <Image> tags
        text = re.sub(
            r'<Image\s+[^>]*src="([^"]*)"[^>]*/?>',
            r"![image](\1)",
            text,
        )

        # <Embed> tags -> link
        text = re.sub(
            r'<Embed\s+[^>]*url="([^"]*)"[^>]*/?>',
            r"[Embedded content](\1)",
            text,
        )

        # <Table> tags - just strip the tags, keep content
        text = re.sub(r"</?Table[^>]*>", "", text)

        # Generic HTML tag cleanup (strip remaining unknown tags)
        text = re.sub(r"</?(?:br|div|span|p|strong|em)[^>]*>", "", text)

        return text

    def _fix_escaped_underscores(self, text):
        r"""Fix escaped underscores like subject\_type -> subject_type."""
        return text.replace("\\_", "_")

    def _fix_doc_links(self, text):
        """Convert (doc:slug) links to readable text."""
        text = re.sub(r"\[([^\]]*)\]\(doc:([^)]*)\)", r"\1", text)
        text = re.sub(r"\(doc:([^)]*)\)", r"(\1)", text)
        return text

    def _normalize_headings(self, text):
        """Ensure content headings start at ## (not #)."""
        lines = text.split("\n")
        result = []
        for line in lines:
            # Don't touch lines inside code blocks
            if line.startswith("# ") and not line.startswith("## "):
                # Convert top-level headings to ##
                result.append("#" + line)
            else:
                result.append(line)
        return "\n".join(result)

    def _clean_blank_lines(self, text):
        """Remove excessive blank lines (more than 2 consecutive)."""
        return re.sub(r"\n{4,}", "\n\n\n", text)


# ---------------------------------------------------------------------------
# ChunkGenerator
# ---------------------------------------------------------------------------
class ChunkGenerator:
    """Generates chunked content from cleaned text or skeleton structure."""

    def auto_chunk(self, cleaned_content, chunk_ids, title):
        """Split content into chunks at ## heading boundaries and wrap with markers."""
        if not cleaned_content.strip():
            return self.generate_skeleton_chunks(chunk_ids, title)

        # Split at ## headings
        sections = self._split_at_headings(cleaned_content)

        if not sections:
            # Single chunk for very short content
            chunk_id = chunk_ids[0] if chunk_ids else "content"
            return self._wrap_chunk(chunk_id, cleaned_content)

        # Generate TL;DR from first section
        tldr = self._generate_tldr(title, cleaned_content)
        result_parts = [self._wrap_chunk("tldr", tldr)]

        # Map sections to chunk IDs
        used_ids = {"tldr"}
        remaining_ids = [
            cid for cid in chunk_ids if cid not in ("tldr", "related-topics")
        ]

        for i, (heading, content) in enumerate(sections):
            # Try to match heading to a chunk ID
            chunk_id = self._match_chunk_id(heading, remaining_ids)
            if chunk_id:
                remaining_ids.remove(chunk_id)
            else:
                chunk_id = self._heading_to_id(heading)

            if chunk_id in used_ids:
                chunk_id = f"{chunk_id}-{i}"
            used_ids.add(chunk_id)

            section_text = f"## {heading}\n\n{content}" if heading else content
            result_parts.append(self._wrap_chunk(chunk_id, section_text))

        # Add related-topics chunk if in chunk_ids
        if "related-topics" in chunk_ids:
            result_parts.append(
                self._wrap_chunk(
                    "related-topics",
                    "## Related Topics\n\n<!-- Add links to related documentation -->",
                )
            )

        return "\n\n".join(result_parts)

    def generate_skeleton_chunks(self, chunk_ids, title):
        """Generate placeholder chunks for skeleton files."""
        parts = []
        for chunk_id in chunk_ids:
            if chunk_id == "tldr":
                content = (
                    f"## TL;DR\n\n<!-- TODO: Add 2-3 sentence summary of {title} -->"
                )
            elif chunk_id == "overview":
                content = (
                    "## Overview\n\n"
                    "**What:** <!-- TODO: One-sentence description -->\n\n"
                    "**When to use:** <!-- TODO: Scenarios -->\n\n"
                    "**Prerequisites:** <!-- TODO: What to know first -->"
                )
            elif chunk_id == "related-topics":
                content = "## Related Topics\n\n<!-- TODO: Add links to related documentation -->"
            else:
                heading = chunk_id.replace("-", " ").title()
                content = f"## {heading}\n\n<!-- TODO: Add content for {chunk_id} -->"
            parts.append(self._wrap_chunk(chunk_id, content))
        return "\n\n".join(parts)

    def _split_at_headings(self, text):
        """Split text into (heading, content) tuples at ## boundaries."""
        sections = []
        current_heading = None
        current_lines = []

        for line in text.split("\n"):
            if line.startswith("## "):
                # Save previous section
                if current_heading is not None or current_lines:
                    sections.append((current_heading, "\n".join(current_lines).strip()))
                current_heading = line[3:].strip()
                current_lines = []
            else:
                current_lines.append(line)

        # Save last section
        if current_heading is not None or current_lines:
            sections.append((current_heading, "\n".join(current_lines).strip()))

        # Filter out empty sections and sections with no heading (preamble text)
        # Keep preamble only if it has substantial content
        result = []
        for heading, content in sections:
            if heading is None:
                if len(content.split()) > 20:  # Keep preamble if substantial
                    result.append(("Overview", content))
            elif content:
                result.append((heading, content))

        return result

    def _generate_tldr(self, title, content):
        """Generate a TL;DR from the title and first paragraph."""
        # Get first substantial paragraph
        paragraphs = content.split("\n\n")
        first_para = ""
        for p in paragraphs:
            p = p.strip()
            if p and not p.startswith("#") and not p.startswith("<!--") and len(p) > 30:
                first_para = p
                break

        if first_para:
            # Truncate to ~2 sentences
            sentences = re.split(r"(?<=[.!?])\s+", first_para)
            summary = " ".join(sentences[:2])
            if len(summary) > 300:
                summary = summary[:297] + "..."
            return f"## TL;DR\n\n{summary}"
        else:
            return f"## TL;DR\n\n{title}. See below for details."

    def _match_chunk_id(self, heading, available_ids):
        """Try to match a heading to an available chunk ID."""
        if not heading:
            return None
        heading_lower = heading.lower().replace(" ", "-")
        heading_words = set(heading.lower().split())

        for cid in available_ids:
            cid_words = set(cid.split("-"))
            # Exact or close match
            if cid in heading_lower or heading_lower in cid:
                return cid
            # Word overlap
            overlap = heading_words & cid_words
            if len(overlap) >= max(1, len(cid_words) - 1):
                return cid
        return None

    def _heading_to_id(self, heading):
        """Convert a heading to a chunk ID."""
        if not heading:
            return "content"
        # Lowercase, replace spaces/special chars with hyphens
        chunk_id = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
        # Limit length
        return chunk_id[:50]

    def _wrap_chunk(self, chunk_id, content):
        """Wrap content in chunk markers."""
        return f"<!-- CHUNK: {chunk_id} -->\n{content}\n<!-- END CHUNK -->"


# ---------------------------------------------------------------------------
# MetadataGenerator
# ---------------------------------------------------------------------------
class MetadataGenerator:
    """Generates YAML frontmatter from manifest entry."""

    REQUIRED_FIELDS = [
        "title",
        "category",
        "audience",
        "difficulty",
        "priority",
        "keywords",
        "last_updated",
    ]
    OPTIONAL_FIELDS = [
        "task_types",
        "features",
        "technical_level",
        "implementation_phase",
        "complexity",
        "query_patterns",
        "answer_types",
        "retrieval_boost",
        "related_topics",
        "prerequisites",
        "estimated_reading_time",
        "version",
    ]

    def generate(self, entry, word_count=0):
        metadata = {}

        # Required fields
        metadata["title"] = entry["title"]
        metadata["category"] = entry["category"]
        metadata["audience"] = entry.get("audience", "implementer")
        metadata["difficulty"] = entry.get("difficulty", "intermediate")
        metadata["priority"] = entry.get("priority", "medium")
        metadata["keywords"] = entry.get("keywords", [])
        metadata["last_updated"] = datetime.now().strftime("%Y-%m-%d")

        # Optional fields
        for field in self.OPTIONAL_FIELDS:
            if field in entry:
                metadata[field] = entry[field]

        # Auto-generate reading time if not present
        if "estimated_reading_time" not in metadata and word_count > 0:
            minutes = max(1, word_count // 200)
            metadata["estimated_reading_time"] = f"{minutes} minutes"

        if "version" not in metadata:
            metadata["version"] = "1.0"

        return (
            "---\n"
            + yaml.dump(
                metadata, default_flow_style=False, sort_keys=False, allow_unicode=True
            )
            + "---"
        )


# ---------------------------------------------------------------------------
# ReadmeGenerator
# ---------------------------------------------------------------------------
class ReadmeGenerator:
    """Generates section README.md files from manifest data."""

    def generate(self, entry, section_entries):
        """Build a section README with navigation."""
        title = entry["title"]
        description = entry.get("section_description", "")

        parts = []
        parts.append(f"# {title}\n")
        parts.append(f"{description}\n")

        parts.append("## Contents\n")

        for i, se in enumerate(section_entries, 1):
            filename = os.path.basename(se["output_path"])
            se_title = se["title"]
            parts.append(f"### {i}. [{se_title}]({filename})")

            # Add a brief description from keywords
            kw = se.get("keywords", [])
            if kw:
                parts.append(f"{'  '.join(kw[:4])}\n")
            else:
                parts.append("")

        return "\n".join(parts)


# ---------------------------------------------------------------------------
# QAFormatter
# ---------------------------------------------------------------------------
class QAFormatter:
    """Format Q&A pairs as FAQ content."""

    @staticmethod
    def format(pairs, max_pairs=10):
        if not pairs:
            return ""

        parts = []
        for q, a in pairs[:max_pairs]:
            parts.append(f"### Q: {q}\n")
            parts.append(f"{a}\n")

        return "\n".join(parts)


# ---------------------------------------------------------------------------
# Main Generator
# ---------------------------------------------------------------------------
class KBGenerator:
    def __init__(
        self,
        manifest_path,
        base_dir,
        output_dir=None,
        dry_run=False,
        skip_existing=False,
    ):
        self.manifest = self._load_manifest(manifest_path)
        self.base_dir = base_dir
        self.output_dir = output_dir or base_dir
        self.dry_run = dry_run
        self.skip_existing = skip_existing

        self.loader = SourceLoader(base_dir)
        self.cleaner = ContentCleaner()
        self.chunker = ChunkGenerator()
        self.meta_gen = MetadataGenerator()
        self.readme_gen = ReadmeGenerator()

    def _load_manifest(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate(self, section_filter=None):
        """Generate all files from manifest."""
        stats = {"generated": 0, "skipped": 0, "errors": 0}

        for entry in self.manifest:
            output_path = entry["output_path"]

            # Section filter
            if section_filter:
                section_prefix = section_filter
                if not section_prefix.endswith("-"):
                    # Match section number prefix like "02" -> "02-"
                    section_prefix = section_filter
                if not output_path.startswith(section_prefix):
                    continue

            full_path = os.path.join(self.output_dir, output_path)

            # Skip existing
            if self.skip_existing and os.path.exists(full_path):
                print(f"  SKIP (exists): {output_path}")
                stats["skipped"] += 1
                continue

            if self.dry_run:
                content_type = entry.get("content_type", "unknown")
                sources = entry.get("sources", [])
                source_info = (
                    ", ".join(
                        f"{s['file']}:{s.get('start_line', '?')}-{s.get('end_line', '?')}"
                        for s in sources
                    )
                    if sources
                    else "none"
                )
                print(
                    f"  WOULD GENERATE: {output_path} [{content_type}] from {source_info}"
                )
                stats["generated"] += 1
                continue

            try:
                content = self._generate_file(entry)
                self._write_file(full_path, content)
                print(f"  GENERATED: {output_path}")
                stats["generated"] += 1
            except Exception as e:
                print(f"  ERROR: {output_path} - {e}")
                stats["errors"] += 1

        return stats

    def _generate_file(self, entry):
        """Generate complete file content for one manifest entry."""
        content_type = entry.get("content_type", "skeleton")
        is_readme = entry.get("is_readme", False)

        if is_readme or content_type == "readme":
            return self._generate_readme(entry)
        elif content_type == "extract":
            return self._generate_extract(entry)
        elif content_type == "synthesize":
            return self._generate_synthesize(entry)
        elif content_type == "skeleton":
            return self._generate_skeleton(entry)
        else:
            raise ValueError(f"Unknown content_type: {content_type}")

    def _generate_readme(self, entry):
        """Generate a section README."""
        # Find all non-readme entries in the same section
        section_dir = os.path.dirname(entry["output_path"])
        section_entries = [
            e
            for e in self.manifest
            if os.path.dirname(e["output_path"]) == section_dir
            and not e.get("is_readme", False)
            and e.get("content_type") != "readme"
        ]

        body = self.readme_gen.generate(entry, section_entries)

        # Generate metadata
        meta_entry = dict(entry)
        meta_entry.setdefault("audience", "implementer")
        meta_entry.setdefault("difficulty", "beginner")
        meta_entry.setdefault("priority", "high")
        meta_entry.setdefault("keywords", [entry["category"]])
        meta_entry.setdefault("task_types", ["reference"])
        meta_entry.setdefault("technical_level", ["conceptual"])
        meta_entry.setdefault("retrieval_boost", 1.0)

        frontmatter = self.meta_gen.generate(meta_entry)
        return frontmatter + "\n" + body

    def _generate_extract(self, entry):
        """Generate file by extracting from source line ranges."""
        sources = entry.get("sources", [])
        title = entry["title"]
        chunk_ids = entry.get(
            "chunks", ["tldr", "overview", "content", "related-topics"]
        )

        # Extract and combine all source content
        raw_parts = []
        for source in sources:
            source_file = source["file"]
            start = source.get("start_line", 1)
            end = source.get("end_line", start + 100)
            raw = self.loader.get_lines(source_file, start, end)
            if raw.strip():
                raw_parts.append(raw)

        if not raw_parts:
            # Fallback to skeleton
            return self._generate_skeleton(entry)

        raw_combined = "\n\n".join(raw_parts)
        cleaned = self.cleaner.clean(raw_combined)

        if not cleaned.strip():
            return self._generate_skeleton(entry)

        # Auto-chunk the cleaned content
        body = self.chunker.auto_chunk(cleaned, chunk_ids, title)

        # Generate metadata
        word_count = len(body.split())
        frontmatter = self.meta_gen.generate(entry, word_count)

        return frontmatter + "\n" + f"# {title}\n\n" + body

    def _generate_synthesize(self, entry):
        """Generate file by combining multiple sources and filtered Q&A pairs."""
        sources = entry.get("sources", [])
        title = entry["title"]
        chunk_ids = entry.get(
            "chunks", ["tldr", "overview", "content", "related-topics"]
        )
        qa_keywords = entry.get("test_prompts_filter", [])

        # Extract source content
        raw_parts = []
        for source in sources:
            source_file = source["file"]
            start = source.get("start_line", 1)
            end = source.get("end_line", start + 100)
            raw = self.loader.get_lines(source_file, start, end)
            if raw.strip():
                raw_parts.append(raw)

        # Add filtered Q&A pairs
        if qa_keywords:
            qa_pairs = self.loader.get_filtered_qa_pairs(qa_keywords)
            if qa_pairs:
                qa_content = QAFormatter.format(qa_pairs)
                if qa_content:
                    raw_parts.append("\n## Frequently Asked Questions\n\n" + qa_content)

        if not raw_parts:
            return self._generate_skeleton(entry)

        raw_combined = "\n\n".join(raw_parts)
        cleaned = self.cleaner.clean(raw_combined)

        if not cleaned.strip():
            return self._generate_skeleton(entry)

        body = self.chunker.auto_chunk(cleaned, chunk_ids, title)

        word_count = len(body.split())
        frontmatter = self.meta_gen.generate(entry, word_count)

        return frontmatter + "\n" + f"# {title}\n\n" + body

    def _generate_skeleton(self, entry):
        """Generate a skeleton file with TODO placeholders."""
        title = entry["title"]
        chunk_ids = entry.get("chunks", ["tldr", "overview", "related-topics"])

        body = self.chunker.generate_skeleton_chunks(chunk_ids, title)

        frontmatter = self.meta_gen.generate(entry)

        return frontmatter + "\n" + f"# {title}\n\n" + body

    def _write_file(self, path, content):
        """Write content to file, creating directories as needed."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Generate Avni AI Assistant Knowledge Base files from manifest"
    )
    parser.add_argument(
        "--manifest",
        default=os.path.join(os.path.dirname(__file__), "file_manifest.json"),
        help="Path to file_manifest.json",
    )
    parser.add_argument(
        "--base-dir",
        default=os.path.join(
            os.path.dirname(__file__), "..", "AI_ASSISTANT_KNOWLEDGE_BASE"
        ),
        help="Base directory for source and output files",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory (defaults to base-dir)",
    )
    parser.add_argument(
        "--section",
        default=None,
        help="Generate only files in this section (e.g., '02' or '03-concepts')",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be generated without writing files",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Don't overwrite files that already exist",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run validation tools after generation",
    )

    args = parser.parse_args()

    base_dir = os.path.abspath(args.base_dir)
    manifest_path = os.path.abspath(args.manifest)
    output_dir = os.path.abspath(args.output_dir) if args.output_dir else base_dir

    print("Knowledge Base Generator")
    print(f"  Manifest: {manifest_path}")
    print(f"  Base dir: {base_dir}")
    print(f"  Output:   {output_dir}")
    print(f"  Section:  {args.section or 'all'}")
    print(f"  Dry run:  {args.dry_run}")
    print(f"  Skip existing: {args.skip_existing}")
    print()

    generator = KBGenerator(
        manifest_path=manifest_path,
        base_dir=base_dir,
        output_dir=output_dir,
        dry_run=args.dry_run,
        skip_existing=args.skip_existing,
    )

    stats = generator.generate(section_filter=args.section)

    print()
    print(
        f"Results: {stats['generated']} generated, {stats['skipped']} skipped, {stats['errors']} errors"
    )

    if args.validate and not args.dry_run:
        print()
        print("Running validation...")
        tools_dir = os.path.dirname(os.path.abspath(__file__))

        print("\n--- Metadata Validation ---")
        subprocess.run(
            [
                sys.executable,
                os.path.join(tools_dir, "validate_metadata.py"),
                output_dir,
            ],
            cwd=tools_dir,
        )

        print("\n--- Chunk Analysis ---")
        subprocess.run(
            [sys.executable, os.path.join(tools_dir, "analyze_chunks.py"), output_dir],
            cwd=tools_dir,
        )


if __name__ == "__main__":
    main()
