"""Validate the portable rule package without installing it or calling services."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ("skill", "radar", "mother", "adapt", "design", "image", "distribute", "feedback")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PRIVATE = re.compile(r"/" + r"Users/[^\s/]+/|(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{15,}|https://[^\s/]+\.feishu\.cn/base/[^\s)]+")


def check(root):
    errors, links = [], 0
    for module in MODULES:
        path = root / f"one-{module}" / "SKILL.md"
        if not path.is_file():
            errors.append(f"missing: {path.relative_to(root)}")
            continue
        text = path.read_text()
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not match or f"name: one-{module}\n" not in match[1] + "\n" or not re.search(r"^description: .+", match[1], re.M):
            errors.append(f"invalid frontmatter: {path.relative_to(root)}")
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts or path.is_dir():
            continue
        if path.is_symlink():
            errors.append(f"symlink: {path.relative_to(root)}")
            continue
        if path.suffix not in {".md", ".yaml", ".json", ".py"}:
            continue
        text = path.read_text()
        if PRIVATE.search(text):
            errors.append(f"private data pattern: {path.relative_to(root)}")
        if path.suffix != ".md":
            continue
        if text.count("```") % 2:
            errors.append(f"unclosed fence: {path.relative_to(root)}")
        for link in LINK.findall(text):
            if link.startswith(("https://", "http://", "#", "mailto:")):
                continue
            target = (path.parent / link.split("#", 1)[0]).resolve()
            if not target.is_relative_to(root.resolve()) or not target.is_file():
                errors.append(f"broken or external local link: {path.relative_to(root)} -> {link}")
            links += 1
    config = root / "config.example.json"
    try:
        data = json.loads(config.read_text())
        assert data["author_samples"] == [] and data["knowledge_paths"] == []
        assert all(value is None for value in data["connections"].values())
    except (OSError, ValueError, KeyError, AssertionError, AttributeError):
        errors.append("invalid or nonempty private config example")
    return {"modules": len(MODULES), "local_links": links, "errors": errors, "pass": not errors}


def self_check():
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "README.md").write_text("[missing](no-file.md)\n")
        result = check(root)
        assert not result["pass"]
        assert any("broken or external local link" in error for error in result["errors"])
        assert any("missing:" in error for error in result["errors"])


if __name__ == "__main__":
    self_check()
    result = check(ROOT)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["pass"] else 1)
