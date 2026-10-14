#!/usr/bin/env python3
"""
Code the Word
Weaves scripture into source code comments, matched to what each block of code does.

Usage:
  python codetheword.py PATH                  preview what would be added (changes nothing)
  python codetheword.py PATH --write          add verses to the files
  python codetheword.py PATH --strip --write  remove every verse this tool added
  python codetheword.py PATH --study          write STUDY.md: every verse in reading order
Options:
  --gap N        minimum lines between verses (default 8; lower = denser)
  --verses FILE  use a different verse map (default: verses.json next to this script)
"""
import argparse
import json
import re
import sys
import textwrap
from pathlib import Path

MARK = "[Word]"

COMMENT_PREFIX = {
    ".py": "#", ".rb": "#", ".sh": "#", ".bash": "#", ".r": "#", ".pl": "#",
    ".yml": "#", ".yaml": "#", ".toml": "#",
    ".js": "//", ".jsx": "//", ".ts": "//", ".tsx": "//", ".mjs": "//", ".cjs": "//",
    ".java": "//", ".kt": "//", ".swift": "//", ".go": "//", ".rs": "//",
    ".c": "//", ".h": "//", ".cpp": "//", ".hpp": "//", ".cs": "//",
    ".php": "//", ".dart": "//", ".scala": "//",
    ".sql": "--", ".lua": "--", ".hs": "--",
}

SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "env", "__pycache__",
             "dist", "build", ".next", "vendor", "target", ".idea", ".vscode"}

# Lines that open a meaningful block of code
BLOCK_START = re.compile(r"""^\s*(?:
      (?:async\s+)?def\s+\w+
    | class\s+\w+
    | (?:export\s+)?(?:default\s+)?(?:async\s+)?function\b
    | (?:export\s+)?(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?(?:\([^)]*\)|\w+)\s*=>
    | func\s+
    | (?:pub(?:\(\w+\))?\s+)?(?:async\s+)?fn\s+\w+
    | (?:struct|interface|trait|impl|enum)\s+\w+
    | try\b
    | (?:for|while)\b.*[:{]\s*$
    | (?:public|private|protected|static|internal)\s[\w<>\[\],\s]*\w+\s*\([^;]*$
)""", re.X)


def words_of(line):
    """Split camelCase / snake_case / punctuation into lowercase words."""
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", line)
    return [w for w in re.split(r"[^A-Za-z]+", spaced.lower()) if w]


class VerseMap:
    def __init__(self, path):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.translation = data.get("translation", "KJV")
        self.categories = data["categories"]
        self.fallback = data["fallback"]
        self.counters = {}

    def _next(self, key, verses):
        i = self.counters.get(key, 0)
        self.counters[key] = i + 1
        return verses[i % len(verses)]

    def pick(self, code_line):
        words = words_of(code_line)
        if not words:
            return "fallback", self._next("fallback", self.fallback)
        lead = words[0]
        # skip declaration words to find the first meaningful leading word
        for w in words:
            if w not in {"export", "default", "async", "public", "private", "protected",
                         "static", "internal", "pub", "const", "let", "var"}:
                lead = w
                break
        # 1) structure: what kind of statement is it?
        for cat in self.categories:
            if lead in cat.get("starts_with", []):
                return cat["name"], self._next(cat["name"], cat["verses"])
        # 2) meaning: what is the function/class named?
        name_words = set(words[1:]) if len(words) > 1 else set(words)
        for cat in self.categories:
            if name_words & set(cat.get("keywords", [])):
                return cat["name"], self._next(cat["name"], cat["verses"])
        return "fallback", self._next("fallback", self.fallback)


def render(prefix, indent, verse, translation):
    out = [f"{indent}{prefix} {MARK} {verse['ref']} ({translation})"]
    for chunk in textwrap.wrap(f"\u201c{verse['text']}\u201d", width=72):
        out.append(f"{indent}{prefix} {MARK} {chunk}")
    if verse.get("note"):
        out.append(f"{indent}{prefix} {MARK} \u21b3 {verse['note']}")
    return out


def is_ours(line, prefix):
    s = line.strip()
    return s.startswith(prefix) and MARK in s


def process_file(path, prefix, vmap, gap, strip):
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None, []
    lines = text.splitlines(keepends=True)
    newline = "\r\n" if "\r\n" in text else "\n"

    if strip:
        kept = [l for l in lines if not is_ours(l, prefix)]
        removed = len(lines) - len(kept)
        return ("".join(kept) if removed else None), [("removed", removed)] if removed else []

    out, added = [], []
    last_insert = -10**9
    in_block_string = False
    py = path.suffix == ".py"

    code_idx = 0  # counts real code lines only, so reruns make the same choices
    for i, line in enumerate(lines):
        stripped = line.strip()
        if is_ours(line, prefix):
            out.append(line)
            continue
        code_idx += 1

        # don't touch anything inside Python docstrings or /* block comments */
        if py:
            if (stripped.count('"""') + stripped.count("'''")) % 2 == 1:
                in_block_string = not in_block_string
                out.append(line)
                continue
        else:
            if "/*" in stripped and "*/" not in stripped:
                in_block_string = True
            elif "*/" in stripped:
                in_block_string = False

        prev_ours = bool(out) and is_ours(out[-1], prefix)
        if prev_ours and BLOCK_START.match(line):
            last_insert = code_idx  # an earlier run already blessed this block
        if (not in_block_string and BLOCK_START.match(line)
                and not stripped.startswith(prefix)
                and not prev_ours
                and code_idx - last_insert >= gap):
            indent = line[: len(line) - len(line.lstrip())]
            category, verse = vmap.pick(stripped)
            for c in render(prefix, indent, verse, vmap.translation):
                out.append(c + newline)
            added.append((i + 1, verse["ref"], category, stripped[:70]))
            last_insert = code_idx
        out.append(line)

    return ("".join(out) if added else None), added


def walk(root):
    root = Path(root)
    if root.is_file():
        yield root
        return
    for p in sorted(root.rglob("*")):
        if p.is_file() and not any(part in SKIP_DIRS for part in p.parts):
            yield p


def build_study(root, out_path):
    entries = []
    root = Path(root)
    for path in walk(root):
        prefix = COMMENT_PREFIX.get(path.suffix.lower())
        if not prefix:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        current = None
        for n, line in enumerate(lines, 1):
            if is_ours(line, prefix):
                body = line.strip()[len(prefix):].strip()[len(MARK):].strip()
                if current is None:
                    current = {"file": str(path.relative_to(root) if root.is_dir() else path.name),
                               "line": n, "ref": body, "text": [], "note": ""}
                elif body.startswith("\u21b3"):
                    current["note"] = body[1:].strip()
                else:
                    current["text"].append(body)
            elif current is not None:
                current["code"] = line.strip()
                entries.append(current)
                current = None
    md = ["# Code the Word: Study Path", "",
          "Every verse hidden in this codebase, in the order you meet it.", ""]
    for i, e in enumerate(entries, 1):
        md.append(f"## {i}. {e['ref']}")
        md.append(f"> {' '.join(e['text'])}")
        md.append("")
        if e["note"]:
            md.append(f"*{e['note']}*")
            md.append("")
        md.append(f"Found at `{e['file']}:{e['line']}` above `{e.get('code', '')}`")
        md.append("")
    Path(out_path).write_text("\n".join(md), encoding="utf-8")
    return len(entries)


def main():
    ap = argparse.ArgumentParser(description="Code the Word: scripture woven into source code.")
    ap.add_argument("path")
    ap.add_argument("--write", action="store_true", help="actually change files")
    ap.add_argument("--strip", action="store_true", help="remove verses this tool added")
    ap.add_argument("--study", action="store_true", help="write STUDY.md from verses already in the code")
    ap.add_argument("--gap", type=int, default=8, help="minimum lines between verses")
    ap.add_argument("--verses", default=str(Path(__file__).with_name("verses.json")))
    args = ap.parse_args()

    if args.study:
        target = Path(args.path)
        out = (target if target.is_dir() else target.parent) / "STUDY.md"
        n = build_study(args.path, out)
        print(f"Wrote {out} with {n} verses.")
        return

    vmap = VerseMap(args.verses)
    total_files = total = 0
    for path in walk(args.path):
        prefix = COMMENT_PREFIX.get(path.suffix.lower())
        if not prefix:
            continue
        new_text, changes = process_file(path, prefix, vmap, args.gap, args.strip)
        if not changes:
            continue
        total_files += 1
        print(f"\n{path}")
        for c in changes:
            if c[0] == "removed":
                print(f"  removed {c[1]} verse lines")
                total += c[1]
            else:
                print(f"  line {c[0]:>5}  {c[1]:<22} [{c[2]}]  {c[3]}")
                total += 1
        if args.write and new_text is not None:
            path.write_text(new_text, encoding="utf-8")

    verb = "removed" if args.strip else "placed"
    mode = "" if args.write else "  (preview only: add --write to apply)"
    print(f"\n{total} {'lines' if args.strip else 'verses'} {verb} across {total_files} files.{mode}")


if __name__ == "__main__":
    main()
