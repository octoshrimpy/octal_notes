"""Note-taking for the terminal, built with Textual."""

__author__ = "Marcos Jones"
__copyright__ = "Copyright Marcos Jones"
__credits__ = ["Marcos Jones"]
__maintainer__ = "Marcos Jones"
__email__ = "octoshrimpy@gmail.com"
__version__ = "0.1.0"
__license__ = "MIT"

# Set version string when in a git repository
# to distinguish production from development versions.

from os.path import dirname, exists
from subprocess import check_output

DEVELOPMENT = exists(dirname(__file__) + "/../../.git")
"""Whether running from a Git repository."""

import sys

PYTEST = "pytest" in sys.modules
"""Whether running from pytest."""

if PYTEST:
    # Avoid version string in About Paint dialog affecting snapshots.
    __version__ = "snapshot test edition :)"
elif DEVELOPMENT:
    __version__ = "development " + check_output(["git", "describe", "--tags"], cwd=dirname(__file__)).strip().decode()
