#!/usr/bin/env python3
"""Build en/index.html from index.html (the IT master) + i18n_strings.py.

Two-way sync — you can edit either side:

* edit `index.html` to change copy or markup → just re-run this script.
* edit `scripts/i18n_strings.py` to refine translations → re-run.
* edit `en/index.html` directly to refine English wording → re-run; this
  script diffs the on-disk EN against what it WOULD regenerate from
  IT + the saved pairs, lifts any hand-edited strings into
  i18n_strings.py, then re-emits a clean EN.

How the lift works: each translation pair has an unambiguous IT key in
index.html. After applying all pairs to IT we get the "expected EN".
Walking expected_EN and existing_EN side-by-side, any place where they
diverge corresponds to exactly one pair (because the gaps between
pairs are common HTML markup). The new EN value is the slice of
existing_EN that occupies the equivalent range.

Workflow on a content change:

    1. edit index.html or en/index.html or scripts/i18n_strings.py
    2. python scripts/build_i18n.py
    3. python scripts/cache-bust.py
    4. git commit + push
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
SRC = ROOT / "index.html"
DST = ROOT / "en" / "index.html"
STRINGS_FILE = SCRIPTS / "i18n_strings.py"

# Make i18n_strings importable when run as a script.
sys.path.insert(0, str(SCRIPTS))
import i18n_strings  # noqa: E402


# ---------------------------------------------------------------------------
# Lang-specific transformations applied *after* translation pairs.
# These are everything that changes between IT and EN that ISN'T plain prose
# (canonical URL, asset paths, language switcher active state, etc.).
# ---------------------------------------------------------------------------

LANG_REPLACEMENTS_ONCE = [
    ('<html lang="it">', '<html lang="en">'),
    ('<link rel="canonical" href="https://www.honeyandfire.band/" />',
     '<link rel="canonical" href="https://www.honeyandfire.band/en/" />'),
    ('property="og:url" content="https://www.honeyandfire.band/"',
     'property="og:url" content="https://www.honeyandfire.band/en/"'),
    # Language switcher: flag active state flips on the EN page.
    ('<li class="nav-lang nav-lang-active" aria-current="page">\n'
     '\t\t\t\t\t\t\t<a href="/" hreflang="it"',
     '<li class="nav-lang">\n\t\t\t\t\t\t\t<a href="/" hreflang="it"'),
    ('<li class="nav-lang">\n\t\t\t\t\t\t\t<a href="/en/" hreflang="en"',
     '<li class="nav-lang nav-lang-active" aria-current="page">\n'
     '\t\t\t\t\t\t\t<a href="/en/" hreflang="en"'),
    ('href="locandina-260521.html"', 'href="../locandina-260521.html"'),
    ('href="honey-and-fire-260521.ics"', 'href="../honey-and-fire-260521.ics"'),
]

LANG_REPLACEMENTS_GLOBAL = [
    ('id="uk-clip-it"', 'id="uk-clip-en"'),
    ("url(#uk-clip-it)", "url(#uk-clip-en)"),
]

# Local asset prefixes — index.html lives at root, en/index.html one level
# deep, so href|src starting with assets/ or images/ get a "../" prefix.
ASSET_PATH_RE = re.compile(r'((?:href|src)=")(assets/|images/)')


def regenerate_en(it_source: str, pairs: list[tuple[str, str]]) -> str:
    """Apply translation pairs + lang-specific transformations to IT."""
    text = it_source

    # 1) Translation pairs — must each match exactly once.
    missing, multi = [], []
    for it_str, en_str in pairs:
        n = text.count(it_str)
        if n == 0:
            missing.append(it_str[:80])
            continue
        if n > 1:
            multi.append((it_str[:80], n))
            continue
        text = text.replace(it_str, en_str, 1)
    if missing or multi:
        for s in missing:
            sys.stderr.write(f"MISSING in source: {s!r}\n")
        for s, n in multi:
            sys.stderr.write(f"AMBIGUOUS ({n}x): {s!r}\n")
        raise SystemExit(2)

    # 2) Once-only lang-specific replacements.
    for src, dst in LANG_REPLACEMENTS_ONCE:
        text = text.replace(src, dst, 1)

    # 3) Asset path prefix.
    text = ASSET_PATH_RE.sub(r"\1../\2", text)

    # 4) Global lang-specific replacements (e.g. SVG clipPath ids).
    for src, dst in LANG_REPLACEMENTS_GLOBAL:
        text = text.replace(src, dst)

    return text


# ---------------------------------------------------------------------------
# Two-way sync — extract hand edits from existing en/index.html.
# ---------------------------------------------------------------------------

def extract_hand_edits(
    expected_en: str,
    existing_en: str,
    pairs: list[tuple[str, str]],
) -> list[tuple[str, str]]:
    """Diff expected vs on-disk EN; return updated pairs that reflect any
    EN-side hand edits."""
    if expected_en == existing_en:
        return pairs

    # Locate each pair's old EN value in expected_en, in source order.
    located = []
    cursor = 0
    for i, (it_str, en_str) in enumerate(pairs):
        pos = expected_en.find(en_str, cursor)
        if pos == -1:
            # The translation didn't make it into expected_en (shouldn't
            # happen because regenerate_en would have already errored).
            continue
        located.append((pos, i, en_str))
        cursor = pos + len(en_str)

    new_pairs = list(pairs)
    e_cursor = 0
    a_cursor = 0
    edits = []

    for idx, (e_pos, pair_index, en_str_old) in enumerate(located):
        # Common region between cursor and this pair, in expected_en.
        common = expected_en[e_cursor:e_pos]
        # Find the same common region in existing_en after a_cursor.
        a_common_pos = existing_en.find(common, a_cursor)
        if a_common_pos == -1:
            print(f"WARN: cannot align pair {pair_index} "
                  f"({pairs[pair_index][0][:50]!r}) — skipping")
            e_cursor = e_pos + len(en_str_old)
            continue
        trans_start = a_common_pos + len(common)
        if existing_en.startswith(en_str_old, trans_start):
            # No hand edit at this position.
            a_cursor = trans_start + len(en_str_old)
        else:
            # Hand edit — find boundary by looking ahead to the NEXT
            # pair's expected position (everything between current
            # pair's end and next pair's start in expected_en is
            # markup that should appear identically in existing_en).
            after_old = e_pos + len(en_str_old)
            if idx + 1 < len(located):
                next_e_pos = located[idx + 1][0]
                next_common = expected_en[after_old:next_e_pos]
            else:
                next_common = expected_en[after_old:]
            boundary = existing_en.find(next_common, trans_start)
            if boundary == -1:
                print(f"WARN: cannot find boundary after pair {pair_index}; "
                      f"leaving unchanged")
                a_cursor = trans_start
            else:
                new_en = existing_en[trans_start:boundary]
                it_str = pairs[pair_index][0]
                new_pairs[pair_index] = (it_str, new_en)
                edits.append((pair_index, en_str_old, new_en, it_str))
                a_cursor = boundary
        e_cursor = e_pos + len(en_str_old)

    if edits:
        print(f"detected {len(edits)} hand edit(s) in en/index.html:")
        for idx, old, new, it_str in edits:
            preview_old = old.replace("\n", " ")[:60]
            preview_new = new.replace("\n", " ")[:60]
            print(f"  · pair {idx}  {preview_old!r}  →  {preview_new!r}")

    return new_pairs


# ---------------------------------------------------------------------------
# Rewriting i18n_strings.py with updated pairs.
# ---------------------------------------------------------------------------

def python_str_literal(s: str) -> str:
    """Format a string as a hand-readable Python literal.

    Single-line strings without quotes use "...". Strings containing
    newlines fall back to repr() with explicit \\n + concatenation,
    matching the style we use in i18n_strings.py for paragraph blocks.
    """
    if "\n" not in s:
        # Prefer double-quoted unless the string contains "
        if '"' in s and "'" not in s:
            return repr(s)  # uses single quotes
        # Use repr to escape any embedded chars consistently.
        return repr(s)
    # Multi-line: emit as concatenation of repr'd lines so the file
    # diff stays readable.
    parts = s.split("\n")
    out = []
    for i, line in enumerate(parts):
        # Preserve the trailing "\n" on every line except the last.
        suffix = "\n" if i < len(parts) - 1 else ""
        out.append(repr(line + suffix))
    return "(" + "\n     ".join(out) + ")"


def write_strings_file(pairs: list[tuple[str, str]]) -> None:
    """Rewrite scripts/i18n_strings.py preserving the docstring at the top
    and emitting one (it, en) tuple per entry."""
    header = STRINGS_FILE.read_text().split("TRANSLATIONS = [", 1)[0]
    chunks = [header, "TRANSLATIONS = [\n"]
    for it_str, en_str in pairs:
        chunks.append("    (\n")
        chunks.append(f"        {python_str_literal(it_str)},\n")
        chunks.append(f"        {python_str_literal(en_str)},\n")
        chunks.append("    ),\n")
    chunks.append("]\n")
    STRINGS_FILE.write_text("".join(chunks))


# ---------------------------------------------------------------------------
# Main.
# ---------------------------------------------------------------------------

def main() -> int:
    pairs = list(i18n_strings.TRANSLATIONS)
    it_source = SRC.read_text()

    # Regenerate the expected EN once so we can sync hand edits.
    expected_en = regenerate_en(it_source, pairs)

    if DST.exists():
        existing_en = DST.read_text()
        if existing_en != expected_en:
            new_pairs = extract_hand_edits(expected_en, existing_en, pairs)
            if new_pairs != pairs:
                write_strings_file(new_pairs)
                print(f"updated {STRINGS_FILE.relative_to(ROOT)}")
                pairs = new_pairs
                expected_en = regenerate_en(it_source, pairs)

    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(expected_en)
    print(f"wrote {DST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
