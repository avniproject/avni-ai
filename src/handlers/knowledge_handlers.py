"""
Knowledge base search handler.

POST /knowledge-search — search Avni documentation using TF-IDF over local markdown files.
"""

import logging
import math
import re
from collections import Counter
from pathlib import Path

from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Knowledge base index (built once at import time)
# ---------------------------------------------------------------------------

_KB_ROOT = (
    Path(__file__).resolve().parent.parent.parent
    / "dify"
    / "knowledge_base"
    / "AI_ASSISTANT_KNOWLEDGE_BASE"
)

# Category mapping from directory names
_DIR_CATEGORIES = {
    "00-getting-started": "getting-started",
    "01-core-concepts": "concepts",
    "02-organization-setup": "setup",
    "03-concepts-and-forms": "forms",
    "04-subject-types-programs": "programs",
    "05-javascript-rules": "rules",
    "06-data-management": "data",
    "07-mobile-app-features": "mobile",
    "08-troubleshooting": "troubleshooting",
    "09-implementation-guides": "implementation",
    "10-reference": "reference",
}


def _tokenize(text: str) -> list[str]:
    """Simple whitespace + punctuation tokenizer, lowercased."""
    return re.findall(r"[a-z0-9]+", text.lower())


class _Document:
    __slots__ = ("path", "source", "category", "title", "content", "tokens", "tf")

    def __init__(self, path: Path, kb_root: Path):
        self.path = path
        rel = path.relative_to(kb_root)
        self.source = str(rel)
        # Derive category from parent directory
        parent_dir = rel.parts[0] if len(rel.parts) > 1 else ""
        self.category = _DIR_CATEGORIES.get(parent_dir, "other")
        # Title from first heading or filename
        self.content = path.read_text(encoding="utf-8", errors="replace")
        heading = re.search(r"^#\s+(.+)", self.content, re.MULTILINE)
        self.title = (
            heading.group(1).strip() if heading else path.stem.replace("-", " ").title()
        )
        # Pre-compute TF
        self.tokens = _tokenize(self.content)
        token_counts = Counter(self.tokens)
        doc_len = len(self.tokens) or 1
        self.tf = {t: c / doc_len for t, c in token_counts.items()}


class _KnowledgeIndex:
    """Simple TF-IDF index over markdown files."""

    def __init__(self, kb_root: Path):
        self.documents: list[_Document] = []
        self.idf: dict[str, float] = {}
        self._build(kb_root)

    def _build(self, kb_root: Path) -> None:
        if not kb_root.exists():
            logger.warning("Knowledge base directory not found: %s", kb_root)
            return

        # Load all markdown files (skip README, merged, _archive)
        for md_path in sorted(kb_root.rglob("*.md")):
            if md_path.name in ("README.md", "merged_kb.md"):
                continue
            if "_archive" in md_path.parts:
                continue
            try:
                doc = _Document(md_path, kb_root)
                if len(doc.tokens) > 10:  # skip near-empty files
                    self.documents.append(doc)
            except Exception as e:
                logger.warning("Failed to index %s: %s", md_path, e)

        # Compute IDF
        n = len(self.documents) or 1
        df: dict[str, int] = Counter()
        for doc in self.documents:
            for token in set(doc.tokens):
                df[token] += 1
        self.idf = {t: math.log(n / (1 + count)) for t, count in df.items()}

        logger.info(
            "Knowledge index built: %d documents, %d unique tokens",
            len(self.documents),
            len(self.idf),
        )

    def search(
        self, query: str, category: str | None = None, top_k: int = 3
    ) -> list[dict]:
        query_tokens = _tokenize(query)
        if not query_tokens:
            return []

        results: list[tuple[float, _Document]] = []
        for doc in self.documents:
            # Category filter
            if category and doc.category != category:
                continue

            # TF-IDF score
            score = 0.0
            for qt in query_tokens:
                tf = doc.tf.get(qt, 0.0)
                idf = self.idf.get(qt, 0.0)
                score += tf * idf

            # Bonus for query terms in title
            title_lower = doc.title.lower()
            for qt in query_tokens:
                if qt in title_lower:
                    score *= 1.5

            if score > 0:
                results.append((score, doc))

        # Sort by score descending
        results.sort(key=lambda x: x[0], reverse=True)

        # Return top_k with truncated content
        output = []
        for score, doc in results[:top_k]:
            # Truncate content to ~2000 chars, preferring the start
            content = doc.content
            if len(content) > 2000:
                content = content[:2000] + "\n\n... (truncated)"
            output.append(
                {
                    "source": doc.source,
                    "title": doc.title,
                    "category": doc.category,
                    "content": content,
                    "score": round(score, 4),
                }
            )

        return output


# Build index at module load time
_index = _KnowledgeIndex(_KB_ROOT)


# ---------------------------------------------------------------------------
# Handler
# ---------------------------------------------------------------------------


async def handle_knowledge_search(request: Request) -> JSONResponse:
    """
    POST /knowledge-search
    Body: { "query": "...", "category": "rules" (optional), "top_k": 3 (optional) }
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    query = body.get("query")
    if not query or not query.strip():
        return JSONResponse({"error": "Missing or empty 'query'"}, status_code=400)

    category = body.get("category")
    top_k = min(int(body.get("top_k", 3)), 5)  # cap at 5

    results = _index.search(query, category=category, top_k=top_k)

    logger.info(
        "knowledge-search: query=%r category=%s top_k=%d results=%d",
        query[:80],
        category,
        top_k,
        len(results),
    )

    return JSONResponse(
        {
            "query": query,
            "category": category,
            "results": results,
            "total_results": len(results),
            "total_documents": len(_index.documents),
        }
    )
