# core/version.py
"""Project version utility.

Provides a single function to retrieve the current version of the project.
"""

# Define the project version. Update this string when releasing a new version.
VERSION = "0.1.0"


def get_version() -> str:
    """Return the current project version.

    Returns:
        str: The version string of the project.
    """
    return VERSION
