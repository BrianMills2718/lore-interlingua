"""Ensure local Markdown references resolve inside the repository.

This is a documentation-integrity check, not verification that external sources
exist or that historical scholarship / metaphysical interpretation is correct.
"""
from pathlib import Path
from urllib.parse import unquote
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^\s)]+)(?:\s+[^)]*)?\)")

class DocumentationReferenceTests(unittest.TestCase):
    def test_relative_markdown_targets_exist(self):
        failures = []
        roots = [ROOT / "README.md", *list((ROOT / "docs").rglob("*.md")),
                 *list((ROOT / "research").rglob("*.md")),
                 *list((ROOT / "experiments").rglob("*.md")),
                 *list((ROOT / "examples").rglob("*.md"))]
        for file in roots:
            text = file.read_text(encoding="utf-8")
            for m in LINK.finditer(text):
                target = unquote(m.group(1)).split("#",1)[0]
                if not target or target.startswith(("https://","http://","mailto:","data:","//")):
                    continue
                if not (file.parent / target).exists():
                    failures.append(f"{file.relative_to(ROOT)} → {target}")
        self.assertFalse(failures, "Unresolved local Markdown targets:\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
