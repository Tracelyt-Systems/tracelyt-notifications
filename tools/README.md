# Repository Tools & Verification Scripts

This directory contains utility and verification scripts used by contributors and CI workflows for `tracelyt-notifications`.

---

## 1. Documentation & Secret Validator (`validate_docs.py`)

A lightweight standard Python script that:
1. Validates that all local relative Markdown links resolve to real files.
2. Checks UTF-8 encoding across repository Markdown files.
3. Scans for accidental credential and private key patterns.

### Usage

```bash
python tools/validate_docs.py
```
*(Returns exit code `0` on success, `1` on broken links or secret pattern matches).*
