#!/usr/bin/env python3
"""
Chunk Size Analyzer for Avni AI Assistant Knowledge Base

Analyzes chunk sizes in markdown files to ensure optimal embedding quality.
Target: 200-600 words per chunk
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def count_words(text: str) -> int:
    """Count words in text."""
    # Remove markdown syntax
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)  # Remove code blocks
    text = re.sub(r"`[^`]+`", "", text)  # Remove inline code
    text = re.sub(r"#+\s", "", text)  # Remove headers
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)  # Remove links, keep text
    text = re.sub(r"[*_]{1,2}([^*_]+)[*_]{1,2}", r"\1", text)  # Remove emphasis

    # Count words
    words = text.split()
    return len(words)


def analyze_chunks(file_path: str) -> List[Tuple[str, int, str]]:
    """Analyze chunks in a markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [("ERROR", 0, f"Error reading file: {e}")]

    # Find all chunks
    chunk_pattern = r"<!-- CHUNK: (.*?) -->(.+?)<!-- END CHUNK -->"
    chunks = re.findall(chunk_pattern, content, re.DOTALL)

    if not chunks:
        return [("NO_CHUNKS", 0, "No chunk markers found in file")]

    results = []
    for chunk_id, chunk_content in chunks:
        word_count = count_words(chunk_content)

        # Determine status
        if word_count < 200:
            status = "⚠️  TOO SHORT"
        elif word_count > 600:
            status = "⚠️  TOO LONG"
        else:
            status = "✅ GOOD"

        results.append((chunk_id, word_count, status))

    return results


def analyze_directory(directory: str) -> dict:
    """Analyze all markdown files in directory."""
    results = {
        "files_with_chunks": [],
        "files_without_chunks": [],
        "chunk_stats": {
            "total_chunks": 0,
            "good_size": 0,
            "too_short": 0,
            "too_long": 0,
        },
    }

    # Find all markdown files
    md_files = list(Path(directory).rglob("*.md"))

    # Exclude certain directories
    exclude_dirs = ["node_modules", ".git", "_archive", "tools"]
    md_files = [f for f in md_files if not any(excl in str(f) for excl in exclude_dirs)]

    for file_path in md_files:
        rel_path = str(file_path.relative_to(directory))
        chunks = analyze_chunks(str(file_path))

        if chunks and chunks[0][0] == "NO_CHUNKS":
            results["files_without_chunks"].append(rel_path)
        elif chunks and chunks[0][0] == "ERROR":
            results["files_without_chunks"].append((rel_path, chunks[0][2]))
        else:
            results["files_with_chunks"].append((rel_path, chunks))

            # Update stats
            for chunk_id, word_count, status in chunks:
                results["chunk_stats"]["total_chunks"] += 1
                if "✅" in status:
                    results["chunk_stats"]["good_size"] += 1
                elif "SHORT" in status:
                    results["chunk_stats"]["too_short"] += 1
                elif "LONG" in status:
                    results["chunk_stats"]["too_long"] += 1

    return results


def print_results(results: dict):
    """Print analysis results."""
    print(f"\n{'=' * 70}")
    print("CHUNK SIZE ANALYSIS RESULTS")
    print(f"{'=' * 70}\n")

    stats = results["chunk_stats"]
    total_files = len(results["files_with_chunks"]) + len(
        results["files_without_chunks"]
    )

    print(f"Total files scanned: {total_files}")
    print(f"Files with chunks: {len(results['files_with_chunks'])}")
    print(f"Files without chunks: {len(results['files_without_chunks'])}")
    print(f"\nTotal chunks: {stats['total_chunks']}")
    print(f"✅ Good size (200-600 words): {stats['good_size']}")
    print(f"⚠️  Too short (<200 words): {stats['too_short']}")
    print(f"⚠️  Too long (>600 words): {stats['too_long']}")

    if stats["total_chunks"] > 0:
        good_pct = (stats["good_size"] / stats["total_chunks"]) * 100
        print(f"\nQuality score: {good_pct:.1f}% chunks are optimal size")

    # Print detailed results for files with issues
    if results["files_with_chunks"]:
        print(f"\n{'=' * 70}")
        print("DETAILED CHUNK ANALYSIS:")
        print(f"{'=' * 70}\n")

        for file_path, chunks in results["files_with_chunks"]:
            has_issues = any("⚠️" in status for _, _, status in chunks)

            if has_issues:
                print(f"\n📄 {file_path}")
                for chunk_id, word_count, status in chunks:
                    print(f"  {status} {chunk_id}: {word_count} words")

    if results["files_without_chunks"]:
        print(f"\n{'=' * 70}")
        print("FILES WITHOUT CHUNK MARKERS:")
        print(f"{'=' * 70}\n")
        for item in results["files_without_chunks"]:
            if isinstance(item, tuple):
                file_path, error = item
                print(f"⚠️  {file_path}: {error}")
            else:
                print(f"⚠️  {item}")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python analyze_chunks.py <directory>")
        print("Example: python analyze_chunks.py ../AI_ASSISTANT_KNOWLEDGE_BASE")
        sys.exit(1)

    directory = sys.argv[1]

    if not Path(directory).exists():
        print(f"Error: Directory '{directory}' does not exist")
        sys.exit(1)

    print(f"Analyzing chunks in: {directory}")
    results = analyze_directory(directory)
    print_results(results)

    # Provide recommendations
    stats = results["chunk_stats"]
    if stats["total_chunks"] > 0:
        good_pct = (stats["good_size"] / stats["total_chunks"]) * 100

        print(f"\n{'=' * 70}")
        print("RECOMMENDATIONS:")
        print(f"{'=' * 70}\n")

        if good_pct >= 80:
            print("✅ Excellent! Most chunks are optimal size for embeddings.")
        elif good_pct >= 60:
            print("⚠️  Good, but some chunks need adjustment.")
            print("   - Split chunks >600 words into smaller sections")
            print("   - Combine chunks <200 words with related content")
        else:
            print("❌ Many chunks need resizing for optimal embeddings.")
            print("   - Target: 300-500 words per chunk")
            print("   - Each chunk should contain one complete concept")
            print("   - Add context so chunks are self-contained")


if __name__ == "__main__":
    main()
