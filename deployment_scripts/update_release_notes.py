

import os
import re
from datetime import datetime
from pathlib import Path


def get_current_version() -> str:
    # Read version file
    VERSION_FILE = Path("__version__.py")
    version_text = VERSION_FILE.read_text()
    # Extract current version string
    match = re.search(r"__version__\s*=\s*['\"](\d+\.\d+\.\d+)['\"]", version_text)
    if not match:
        raise ValueError("Could not find __version__ in file.")
    return match.group(1)


def update_release_notes() -> None:
    
    # Read the environment variables that were passed in from
    # the GitHub Action workflow.
    pr_title: str = os.environ.get("PR_TITLE", "").strip()
    pr_body: str = os.environ.get("PR_BODY", "").strip()
    # Check for missing environment variables
    if not pr_title:
        raise ValueError("PR_TITLE environment variable is missing.")

    # Get current version from version file
    version: str = get_current_version()

    # Create release note entry
    date_str: str = datetime.utcnow().strftime("%Y-%m-%d")
    entry_lines: list[str] = [
        "",
        f"## Release Notes — v{version} — {pr_title} ({date_str})",
        "",
        pr_body,
        "",
    ]

    # Append to README
    with open("README.md", "a", encoding="utf-8") as f:
        f.write("\n".join(entry_lines))

    print("README updated with release notes.")

if __name__ == "__main__":
    update_release_notes()
