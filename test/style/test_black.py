import subprocess
from test.util import PYTHON_FILES_ABSOLUTE, PYTHON_FILES_RELATIVE

import pytest


@pytest.mark.style
@pytest.mark.parametrize(
    "file_path",
    PYTHON_FILES_ABSOLUTE,
    ids=PYTHON_FILES_RELATIVE,
)
def test_black(file_path):
    result = subprocess.run(
        ["black", "--check", "--diff", str(file_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(f"Bad style - Reformat with Black.")
