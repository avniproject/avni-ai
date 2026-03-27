#!/usr/bin/env python3
"""
Merge all knowledge base markdown files into a single file for Dify import.

Walks the KB directory in section order (00 through 10), reads each .md file,
strips YAML frontmatter and chunk markers, and appends to a single output file
with clear section separators.

Usage:
  python3 merge_kb.py                              # Default output: merged_kb.md
  python3 merge_kb.py --output my_kb.md             # Custom output path
  python3 merge_kb.py --keep-metadata               # Retain YAML frontmatter
  python3 merge_kb.py --keep-chunks                  # Retain chunk markers
"""

import argparse
import os
import re


SECTION_ORDER = [
    "00-getting-started",
    "01-core-concepts",
    "02-organization-setup",
    "03-concepts-and-forms",
    "04-subject-types-programs",
    "05-javascript-rules",
    "06-data-management",
    "07-mobile-app-features",
    "08-troubleshooting",
    "09-implementation-guides",
    "10-reference",
]

SKIP_DIRS = {"_archive", "tools", "node_modules", ".git"}


def strip_yaml_frontmatter(text):
    """Remove YAML frontmatter (--- ... ---) from the start of a file."""
    if not text.startswith("---"):
        return text
    # Find closing ---
    end = text.find("\n---", 3)
    if end == -1:
        return text
    # Skip past the closing --- and any trailing newline
    return text[end + 4 :].lstrip("\n")


def strip_chunk_markers(text):
    """Remove <!-- CHUNK: ... --> and <!-- END CHUNK --> markers."""
    text = re.sub(r"<!-- CHUNK: [^\n]* -->\n?", "", text)
    text = re.sub(r"<!-- END CHUNK -->\n?", "", text)
    return text


def get_files_in_order(section_dir):
    """Return markdown files in a section, README first, then alphabetical."""
    if not os.path.isdir(section_dir):
        return []

    files = []
    readme = None

    for f in sorted(os.listdir(section_dir)):
        if not f.endswith(".md"):
            continue
        if f == "README.md":
            readme = os.path.join(section_dir, f)
        else:
            files.append(os.path.join(section_dir, f))

    # README first
    result = []
    if readme:
        result.append(readme)
    result.extend(files)
    return result


def section_display_name(section_dir_name):
    """Convert '03-concepts-and-forms' to 'Concepts And Forms'."""
    # Strip number prefix
    name = re.sub(r"^\d+-", "", section_dir_name)
    return name.replace("-", " ").title()


def merge_kb(kb_dir, output_path, keep_metadata=False, keep_chunks=False):
    """Merge all KB files into a single markdown file."""
    parts = []
    file_count = 0
    total_words = 0

    # Root README first
    root_readme = os.path.join(kb_dir, "README.md")
    if os.path.exists(root_readme):
        with open(root_readme, "r", encoding="utf-8") as f:
            content = f.read()
        if not keep_metadata:
            content = strip_yaml_frontmatter(content)
        if not keep_chunks:
            content = strip_chunk_markers(content)
        parts.append(content.strip())
        file_count += 1
        total_words += len(content.split())

    # Process each section in order
    for section in SECTION_ORDER:
        section_path = os.path.join(kb_dir, section)
        if not os.path.isdir(section_path):
            continue

        section_name = section_display_name(section)
        separator = f"\n\n{'=' * 80}\n# Section: {section_name}\n{'=' * 80}\n"
        parts.append(separator)

        files = get_files_in_order(section_path)
        for filepath in files:
            rel_path = os.path.relpath(filepath, kb_dir)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            if not keep_metadata:
                content = strip_yaml_frontmatter(content)
            if not keep_chunks:
                content = strip_chunk_markers(content)

            content = content.strip()
            if not content:
                continue

            # Add file separator
            file_separator = f"\n\n---\n<!-- Source: {rel_path} -->\n"
            parts.append(file_separator)
            parts.append(content)

            file_count += 1
            total_words += len(content.split())

    # Also pick up any .md files in root that aren't README or in SKIP_DIRS
    for f in sorted(os.listdir(kb_dir)):
        full = os.path.join(kb_dir, f)
        if f == "README.md" or not f.endswith(".md") or os.path.isdir(full):
            continue
        if any(f.startswith(skip) for skip in SKIP_DIRS):
            continue

        with open(full, "r", encoding="utf-8") as fh:
            content = fh.read()

        if not keep_metadata:
            content = strip_yaml_frontmatter(content)
        if not keep_chunks:
            content = strip_chunk_markers(content)

        content = content.strip()
        if content:
            parts.append(f"\n\n---\n<!-- Source: {f} -->\n")
            parts.append(content)
            file_count += 1
            total_words += len(content.split())

    # Assemble
    merged = "\n".join(parts)

    # Clean up excessive blank lines
    merged = re.sub(r"\n{4,}", "\n\n\n", merged)

    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(merged)

    return file_count, total_words, len(merged)


def main():
    parser = argparse.ArgumentParser(
        description="Merge Avni AI KB files into a single markdown for Dify import"
    )
    parser.add_argument(
        "--kb-dir",
        default=os.path.join(
            os.path.dirname(__file__), "..", "AI_ASSISTANT_KNOWLEDGE_BASE"
        ),
        help="Path to knowledge base directory",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: <kb-dir>/merged_kb.md)",
    )
    parser.add_argument(
        "--keep-metadata",
        action="store_true",
        help="Keep YAML frontmatter in output",
    )
    parser.add_argument(
        "--keep-chunks",
        action="store_true",
        help="Keep chunk markers in output",
    )

    args = parser.parse_args()

    kb_dir = os.path.abspath(args.kb_dir)
    output_path = args.output or os.path.join(kb_dir, "merged_kb.md")
    output_path = os.path.abspath(output_path)

    print("Merging Knowledge Base")
    print(f"  KB dir:  {kb_dir}")
    print(f"  Output:  {output_path}")
    print(f"  Keep metadata: {args.keep_metadata}")
    print(f"  Keep chunks:   {args.keep_chunks}")
    print()

    file_count, word_count, byte_count = merge_kb(
        kb_dir,
        output_path,
        keep_metadata=args.keep_metadata,
        keep_chunks=args.keep_chunks,
    )

    size_kb = byte_count / 1024
    size_mb = size_kb / 1024

    print("Done!")
    print(f"  Files merged: {file_count}")
    print(f"  Total words:  {word_count:,}")
    print(f"  Output size:  {size_kb:.0f} KB ({size_mb:.2f} MB)")
    print(f"  Output file:  {output_path}")


if __name__ == "__main__":
    main()
