import subprocess
import sys

from scheduled_tests import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "scheduled_tests", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
