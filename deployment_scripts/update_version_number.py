
"""
Bumps the version number in the `__version__.py` file when a Pull
Request is created.
"""


import re
import os
from pathlib import Path
from typing import Any, Literal

    
def get_current_version(version_text:str) -> str:
    # Extract current version string
    match = re.search(r"__version__\s*=\s*['\"](\d+\.\d+\.\d+)['\"]", version_text)
    if not match:
        raise ValueError("Could not find __version__ in file.")
    return match.group(1)

def get_release_type() -> Literal["patch", "minor", "major"]:
    """ Determine the type of release based on the PR title """
    
    # Read release title from env
    pr_title: str = os.environ.get("PR_TITLE", "").strip()
    # Determine release type based on terms in title
    if "minor" in pr_title.lower():
        return "minor"
    elif "major" in pr_title.lower():
        return "major"
    else:
        return "patch"

def bump_version():
    
    # Read version file
    VERSION_FILE = Path("__version__.py")
    version_text = VERSION_FILE.read_text()

    old_version: str = get_current_version(version_text)
    major, minor, patch = map(int, old_version.split("."))

    # Increment based on the requested level
    level: Literal['patch', 'minor', 'major'] = get_release_type()
    if level == "patch":
        patch += 1
    elif level == "minor":
        minor += 1
        patch = 0
    elif level == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError("level must be 'major', 'minor', or 'patch'")

    new_version = f"{major}.{minor}.{patch}"

    # Replace the version string in the file
    new_text = version_text.replace(old_version,new_version)

    VERSION_FILE.write_text(new_text)
    print(f"Version bumped to {new_version}")
    return new_version




if __name__ == "__main__":
    bump_version()
