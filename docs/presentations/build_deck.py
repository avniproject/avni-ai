#!/usr/bin/env python3.13
"""
build_deck.py — Append an "avni-skills-sdk" learnings section to the existing
"Lessons from Avni App Configurator" deck.

It loads the existing 12-slide deck, clones representative slides at the XML level
(so fonts / colours / positions / accent bars are preserved exactly), swaps the
text by *shape index*, embeds the avni-skills-sdk README screenshots as full-bleed
picture slides, and writes a NEW .pptx. The source deck is never modified.

Run:  python3.13 docs/presentations/build_deck.py
Out:  docs/presentations/avni-skills-sdk-lessons.pptx

Templates used from the source deck (0-based slide index in parentheses):
  slide 1  (0)  -> title / section divider
  slide 6  (5)  -> two-column lesson + glue strip + takeaway
  slide 8  (7)  -> 4 top cards + 5 archetype mini-cards + takeaway
  slide 9  (8)  -> full-bleed picture + caption
  slide 10 (9)  -> 3x2 six-card grid + before/after + takeaway
  slide 12 (11) -> two-column roadmap + top banner + bottom line

Deck structure (this revision):
  AI-stream learnings — "From Dify to Claude-managed agents". Five lessons:
    Stage 1 (deterministic):  L1 spec generation · L2 dependency graph · L3 knowledge base
    Stage 2 (agentic SDK):    L4 history+safety+cost · L5 tools+observability
  Framed as learnings (work in progress); screenshots carry the progress story.
"""
import copy
import os
from pptx import Presentation
from pptx.util import Inches, Emu
from pptx.oxml.ns import qn

SRC = "/tmp/avni_existing_deck.pptx"
SHOTS = "/tmp/avni_shots"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "avni-skills-sdk-lessons.pptx")

GREEN = "2E7D32"
INK = "1F1F1F"

prs = Presentation(SRC)
ORIG_COUNT = len(prs.slides)

# BLANK layout (master0/layout0)
BLANK = None
for layout in prs.slide_masters[0].slide_layouts:
    if layout.name == "BLANK":
        BLANK = layout
        break
assert BLANK is not None, "BLANK layout not found"


def clone_slide(src_slide):
    """Create a new slide that is a deep copy of src_slide's shape tree + background."""
    new_slide = prs.slides.add_slide(BLANK)
    # copy slide-level background if the source defines one
    src_cSld = src_slide._element.find(qn("p:cSld"))
    new_cSld = new_slide._element.find(qn("p:cSld"))
    src_bg = src_cSld.find(qn("p:bg"))
    if src_bg is not None and new_cSld.find(qn("p:bg")) is None:
        new_cSld.insert(0, copy.deepcopy(src_bg))
    # copy every shape from the source spTree into the new spTree
    src_spTree = src_slide.shapes._spTree
    new_spTree = new_slide.shapes._spTree
    for child in list(src_spTree):
        tag = child.tag
        # keep the layout-provided nvGrpSpPr / grpSpPr already in the new spTree;
        # only copy actual shape elements
        if tag in (qn("p:sp"), qn("p:pic"), qn("p:graphicFrame"),
                   qn("p:cxnSp"), qn("p:grpSp")):
            new_spTree.append(copy.deepcopy(child))
    return new_slide


def set_text(slide, idx, text, color=None):
    """Replace the text of shape #idx, preserving the first run's rPr and first
    paragraph's pPr. Lines (\n) become <a:br/>-separated runs in one paragraph.
    Optional `color` recolours the solidFill of every produced run."""
    shape = slide.shapes[idx]
    txBody = shape.text_frame._txBody
    paras = txBody.findall(qn("a:p"))

    tmpl_rPr = None
    for p in paras:
        r = p.find(qn("a:r"))
        if r is not None and r.find(qn("a:rPr")) is not None:
            tmpl_rPr = copy.deepcopy(r.find(qn("a:rPr")))
            break
    tmpl_pPr = None
    if paras and paras[0].find(qn("a:pPr")) is not None:
        tmpl_pPr = copy.deepcopy(paras[0].find(qn("a:pPr")))

    for p in list(paras):
        txBody.remove(p)

    new_p = txBody.makeelement(qn("a:p"), {})
    if tmpl_pPr is not None:
        new_p.append(copy.deepcopy(tmpl_pPr))
    for i, line in enumerate(text.split("\n")):
        if i > 0:
            new_p.append(new_p.makeelement(qn("a:br"), {}))
        r = new_p.makeelement(qn("a:r"), {})
        if tmpl_rPr is not None:
            rPr = copy.deepcopy(tmpl_rPr)
        else:
            rPr = r.makeelement(qn("a:rPr"), {"lang": "en-US"})
        if color is not None:
            for sf in rPr.findall(qn("a:solidFill")):
                for c in sf.findall(qn("a:srgbClr")):
                    c.set("val", color)
        r.append(rPr)
        t = r.makeelement(qn("a:t"), {})
        t.text = line
        r.append(t)
        new_p.append(r)
    txBody.append(new_p)


def add_image_slide(png_name, caption):
    """Clone the picture-slide template (slide 9), strip its embedded picture,
    set the caption, and add the screenshot full-bleed below the caption."""
    src = prs.slides[8]  # slide 9 (0-based 8)
    slide = clone_slide(src)
    # remove any copied <p:pic> (its r:embed would be dangling in the new part)
    spTree = slide.shapes._spTree
    for pic in spTree.findall(qn("p:pic")):
        spTree.remove(pic)
    # set the caption (the remaining text shape)
    for i, sh in enumerate(slide.shapes):
        if sh.has_text_frame and sh.text_frame.text.strip():
            set_text(slide, i, caption)
            break
    # add the screenshot, fit within the area below the caption, centred
    top0 = Inches(0.99)
    max_w = prs.slide_width
    max_h = prs.slide_height - top0
    pic = slide.shapes.add_picture(os.path.join(SHOTS, png_name), 0, top0)
    scale = min(max_w / pic.width, max_h / pic.height)
    tw, th = int(pic.width * scale), int(pic.height * scale)
    pic.width, pic.height = tw, th
    pic.left = int((prs.slide_width - tw) / 2)
    pic.top = int(top0 + (max_h - th) / 2)
    return slide


def six_card_grid(title, subtitle, footer, intro, cards, before, now, takeaway):
    """Clone the 3x2 six-card grid (slide 10) and fill all 6 cards + the
    before / now / takeaway strip. `cards` = list of 6 (title, body) tuples."""
    s = clone_slide(prs.slides[9])
    set_text(s, 1, title)
    set_text(s, 2, subtitle)
    set_text(s, 3, footer)
    set_text(s, 5, intro)
    slots = [(7, 8), (10, 11), (13, 14), (16, 17), (19, 20), (22, 23)]
    for (ti, bi), (ct, cb) in zip(slots, cards):
        set_text(s, ti, ct)
        set_text(s, bi, cb)
    set_text(s, 25, before)
    set_text(s, 26, now)
    set_text(s, 27, takeaway)
    return s


def four_card_grid(title, subtitle, footer, intro, cards, before, now, takeaway):
    """Clone the six-card grid but render only 4 cards as a centred 2x2: keep
    grid slots 1,2,4,5; delete slots 3 & 6 (background box + title + body each);
    shift the kept cards right so the 2x2 is horizontally centred. Keeps the
    before / now / takeaway strip. `cards` = list of 4 (title, body) tuples."""
    s = clone_slide(prs.slides[9])
    set_text(s, 1, title)
    set_text(s, 2, subtitle)
    set_text(s, 3, footer)
    set_text(s, 5, intro)
    keep_slots = [(7, 8), (10, 11), (16, 17), (19, 20)]  # row1 L/M, row2 L/M
    for (ti, bi), (ct, cb) in zip(keep_slots, cards):
        set_text(s, ti, ct)
        set_text(s, bi, cb)
    set_text(s, 25, before)
    set_text(s, 26, now)
    set_text(s, 27, takeaway)
    # centre the kept 2x2: shift bg+title+body of slots 1,2,4,5 right.
    # kept span = cols 1..2 (0.8 -> 8.6 = 7.8in); centre it on the slide.
    kept_shapes = [s.shapes[i] for i in (6, 7, 8, 9, 10, 11, 15, 16, 17, 18, 19, 20)]
    dx = int((prs.slide_width - Inches(7.8)) / 2) - Inches(0.8)
    for sh in kept_shapes:
        sh.left = sh.left + dx
    # delete unused cards (capture elements by index BEFORE removing any):
    #   slot 3 = bg 12, title 13, body 14   ·   slot 6 = bg 21, title 22, body 23
    for el in [s.shapes[i]._element for i in (12, 13, 14, 21, 22, 23)]:
        el.getparent().remove(el)
    return s


# ───────────────────────── slide 13 — section divider (clone slide 1) ─────────
s = clone_slide(prs.slides[0])
set_text(s, 1, "THE NEXT CHAPTER  ·  FROM DIFY TO CLAUDE-MANAGED AGENTS")
set_text(s, 2, "avni-skills-sdk")
set_text(s, 3, "Claude-managed agents, in production")
set_text(s, 4, "“Claude Code, but for an AVNI bundle author”")

# ───────────────────────── slide 14 — new architecture (clone slide 6) ────────
s = clone_slide(prs.slides[5])
set_text(s, 1, "The New Architecture  —  two stages, one workflow")
set_text(s, 2, "System-level  ·  deterministic generator  +  Claude Agent SDK refinement loop")
set_text(s, 3, "avni-skills-sdk  ·  overview")
set_text(s, 5, "Forms.xlsx + Modelling.xlsx in. Ready-for-AVNI bundle out. The LLM only refines.")
set_text(s, 7, "Stage 1  ·  Deterministic")
set_text(s, 8, "•  No LLM  ·  < 1 s  ·  free\n•  2 Excel files → 30+ JSON + zip\n•  Reproducible, auditable bundles\n•  Runs the validator, not a model\n\ne.g.  parse  ·  generate  ·  validate")
set_text(s, 10, "Stage 2  ·  Chat-driven refinement")
set_text(s, 11, "•  Claude Agent SDK loop\n•  Each turn becomes a git commit\n•  Validator runs after every turn\n•  Correct, extend, ship — in chat\n\ne.g.  fix C5  ·  add subject  ·  rename")
set_text(s, 13, "THE BRIDGE  —  slide 12’s “moving to Claude-managed agents,” realized")
set_text(s, 14, "deterministic rails stay free & fast  ·  agentic judgement now audited, capped, reversible")
set_text(s, 15, "Same thesis as before  —  now without Dify.")

# ───────────────────────── slide 15 — image 01 ────────────────────────────────
add_image_slide("01-multi-step-build.png",
                "Multi-step build  —  tools run before every edit")

# ───────────────────────── slide 16 — Building block 1: spec generation (grid) ────────
six_card_grid(
    "Building block 1  —  spec in, bundle out, round-trip",
    "Stage 1  ·  deterministic  ·  avni-skills",
    "avni-skills  ·  1 / 5",
    "One human-readable YAML spec compiles to a full Avni bundle — and decompiles back. Edits patch the live bundle; they never regenerate it.",
    [
        ("Spec → bundle", "YAML parses to entities;\ngenerator emits 30+ JSON files."),
        ("Bundle → spec", "Emitter reverses it; parse→emit\nis byte-equivalent."),
        ("Patch, don’t regen", "New spec merges onto the live\nbundle — UUIDs + UI edits kept."),
        ("Deterministic IDs", "Hash-seeded UUIDs. Same spec\n→ same bundle, every run."),
        ("Canonical ZIP order", "Files in server load order.\nNo silent import failures."),
        ("21-org schema", "Reverse-engineered from 21\nprod orgs. Zero missed keys."),
    ],
    "Before  —  bundles hand-built in the UI or regenerated from scratch; edits and UUIDs lost.",
    "Now  —  a versioned spec compiles, round-trips, and patches in place.",
    "The bundle is a build artifact of a spec — not a hand-edited blob.",
)

# ───────────────────────── slide 17 — Building block 2: dependency graph (grid) ───────
six_card_grid(
    "Building block 2  —  bundle must adhere to a graph",
    "Stage 1  ·  deterministic  ·  avni-skills",
    "avni-skills  ·  2 / 5",
    "Model the bundle as a UUID graph of foreign keys. Then you can ask what depends on what — and catch broken references before the server ever sees them.",
    [
        ("Every entity a node", "Concepts, forms, programs,\nmappings — keyed by UUID."),
        ("Every link an edge", "Typed references: form element\n→ concept, mapping → program."),
        ("Impact check", "What breaks if I delete this?\nSee it first."),
        ("Prerequisites", "What must already exist\nfor this to be valid?"),
        ("Broken-link scan", "Flags every reference\nto a missing UUID."),
        ("Form-type aware", "Knows a program encounter\nneeds a program + type."),
    ],
    "Before  —  dangling references slipped through and failed silently on upload.",
    "Now  —  integrity is checked locally; delete-impact is visible before you act.",
    "Know what breaks before it breaks.",
)

# ───────────────────────── slide 18 — Building block 3: knowledge base (grid) ─────────
six_card_grid(
    "Building block 3  —  knowledge the agent can actually use",
    "Knowledge corpus  ·  avni-readme · avni-ai · avni-skills",
    "knowledge base  ·  3 / 5",
    "Three sources — implementer docs, a merged corpus, and patterns mined from real bundles — compressed into chunked, tagged knowledge the agent pulls on demand.",
    [
        ("Docs as source", "203 implementer guides\n(~21k lines) from avni-readme."),
        ("Merged corpus", "Assembled into merged.md —\n~557 KB, ~22.5k lines."),
        ("Compressed + chunked", "Split into 68 topic files\nwith semantic chunks."),
        ("Metadata-tagged", "Keywords, audience,\nretrieval-boost per chunk."),
        ("Patterns from prod", "4,949 concepts + 132 rule\ntemplates mined from real orgs."),
        ("Retrieval-ready", "Agent pulls the right topic,\nnot the whole monolith."),
    ],
    "Before  —  one 557 KB monolith; retrieval dragged in noise — ~half was infra/reporting.",
    "Now  —  68 focused, tagged topics (~96% implementer) + mined patterns.",
    "Compress for retrieval — high signal beats raw volume.",
)

# ───────────────────────── slide 19 — image 03 ────────────────────────────────
add_image_slide("03-validator-state-and-model-switch.png",
                "Validator-state injection  +  :model switching mid-session")

# ───────────────────────── slide 20 — Building block 4: history+safety+cost (2x2) ─────
four_card_grid(
    "Building block 4  —  logged, gated, capped",
    "Stage 2  ·  agentic SDK  ·  avni-skills-sdk",
    "avni-skills-sdk  ·  4 / 5",
    "Assume the agent will try everything. Make every turn recorded, every destructive path blocked, and every dollar capped — by construction, not by trust.",
    [
        ("Git-backed history", "One commit per turn — a git repo.\nDiff, revert, or resume any turn."),
        ("Audit by construction", "Validator state in every prompt;\nself-corrects on resume; durable."),
        ("Destructive ops gated", "Hook blocks git / rm -rf / sudo;\na detector reverts foreign commits."),
        ("Cost capped", "Hard wallet: $5/session, $1/turn;\naborts a no-edit token spree."),
    ],
    "Before  —  state lived in chat memory; an agent could wander or burn the budget.",
    "Now  —  every turn is git-backed and auditable; destructive paths gated; spend capped.",
    "Audit-rigorous and bounded — by construction.",
)

# ───────────────────────── slide 21 — Building block 5: tools+observability (2x2) ─────
four_card_grid(
    "Building block 5  —  prefer the tools, observe everything",
    "Stage 2  ·  agentic SDK  ·  avni-skills-sdk",
    "avni-skills-sdk  ·  5 / 5",
    "Give the agent purpose-built tools it reaches for instead of raw shell — and make everything it does observable, three ways.",
    [
        ("Prefer tools over shell", "Four in-process bundle tools:\nvalidate, find-concept, summary, export."),
        ("Determinism on rails", "Deterministic :summary handles routine;\nLLM :eval audits the gaps."),
        ("Captured three ways", "On-disk JSONL, live HTTP\nendpoints, and REPL commands."),
        ("See it live", "A live dashboard: per-agent\ncost and failures by category."),
    ],
    "Before  —  the agent improvised with shell; runs were opaque and hard to debug.",
    "Now  —  it prefers a few bundle tools, and every action is logged, served, inspectable.",
    "Deterministic checks on rails; LLM judgement only in the gaps.",
)

# ───────────────────────── slide 22 — image 05 ────────────────────────────────
add_image_slide("05-regression-and-eval.png",
                "Regression detection  +  :eval LLM semantic audit")

# ───────────────────────── slide 23 — image 02 (closer) ───────────────────────
add_image_slide("02-success-and-zip.png",
                "One bundle, end to end  ·  :zip export  ·  $0.13")

prs.save(OUT)
print(f"OK  wrote {OUT}")
print(f"    slides: {ORIG_COUNT} original + {len(prs.slides) - ORIG_COUNT} new = {len(prs.slides)} total")
