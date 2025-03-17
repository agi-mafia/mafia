import subprocess
from test.util import PROJECT_ROOT

import pytest


@pytest.mark.parametrize(
    "file_path",
    list(PROJECT_ROOT.rglob("*.py")),
    ids=lambda file_path: str(file_path.relative_to(PROJECT_ROOT)),
)
def test_style(file_path):
    result = subprocess.run(
        ["black", "--check", "--diff", str(file_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(f"Bad style - Reformat with Black.")
