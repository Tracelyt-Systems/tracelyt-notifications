#!/usr/bin/env python3
"""
Documentation and Repository Integrity Validator for Tracelyt Notifications.

This script executes lightweight static validation:
1. Checks that all relative Markdown links resolve to existing files.
2. Verifies UTF-8 encoding across all documentation files.
3. Scans for accidental secret-like patterns.
4. Exits with 0 on success, 1 on errors.

Dependencies: Python 3.10+ standard library (no external packages required).
"""

import os
import re
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Regex to detect relative markdown links: [text](path)
MD_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

# Basic regex heuristics for accidental credential leaks
SECRET_PATTERNS = [
    re.compile(r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----'),
    re.compile(r'(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36}'),
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'(?:api[_-]?key|secret|password)\s*[:=]\s*["\'](?!example|synthetic|placeholder|changeme|safe-mock)[A-Za-z0-9+/=]{16,}["\']', re.IGNORECASE),
]


def check_markdown_links() -> int:
    """Validate that local relative links in Markdown files resolve to existing files."""
    errors = 0
    md_files = list(REPO_ROOT.glob("**/*.md"))

    for md_path in md_files:
        if "target" in md_path.parts or ".git" in md_path.parts:
            continue

        try:
            content = md_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            print(f"  [ERROR] Non-UTF-8 encoding in {md_path.relative_to(REPO_ROOT)}: {exc}")
            errors += 1
            continue

        for match in MD_LINK_PATTERN.finditer(content):
            target = match.group(2).strip()

            # Skip web URLs, anchors, mailto, and special protocols
            if target.startswith(("http://", "https://", "mailto:", "#", "javascript:")):
                continue

            # Strip target anchors (e.g., path/to/doc.md#section)
            clean_target = target.split("#")[0].strip()
            if not clean_target:
                continue

            if clean_target.startswith("file://"):
                path_str = urllib.request.url2pathname(
                    clean_target[7:] if clean_target.startswith("file:///") else clean_target[7:]
                )
                resolved_path = Path(path_str).resolve()
            elif clean_target.startswith("/"):
                resolved_path = (REPO_ROOT / clean_target.lstrip("/")).resolve()
            else:
                resolved_path = (md_path.parent / clean_target).resolve()

            if not resolved_path.exists():
                print(
                    f"  [ERROR] Broken relative link in {md_path.relative_to(REPO_ROOT)}: "
                    f"'{target}' -> '{resolved_path}' does not exist"
                )
                errors += 1

    return errors


def scan_for_secrets() -> int:
    """Scan tracked repository files for accidental secret patterns."""
    errors = 0
    scannable_exts = {".md", ".yml", ".yaml", ".json", ".java", ".py", ".xml"}

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("target", "tmp")]
        for file_name in files:
            file_path = Path(root) / file_name
            if file_path.suffix not in scannable_exts:
                continue
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                for pattern in SECRET_PATTERNS:
                    if pattern.search(content):
                        print(f"  [SECURITY ALERT] Potential secret pattern matched in {file_path.relative_to(REPO_ROOT)}")
                        errors += 1
            except Exception as exc:
                print(f"  [WARNING] Unable to scan {file_path.relative_to(REPO_ROOT)}: {exc}")

    return errors


def main() -> int:
    print("=== Starting Tracelyt Notifications Documentation & Secret Integrity Verification ===")

    print("\n1. Checking Markdown relative link integrity...")
    link_errors = check_markdown_links()

    print("\n2. Scanning for credentials and sensitive patterns...")
    sec_errors = scan_for_secrets()

    total_errors = link_errors + sec_errors
    if total_errors > 0:
        print(f"\n[FAIL] Validation failed with {total_errors} error(s).")
        return 1

    print("\n[SUCCESS] All documentation integrity and secret checks passed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
