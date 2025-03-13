import subprocess
import pytest
import pathlib
import importlib.util


def get_project_root():
    module_spec = importlib.util.find_spec("src")
    if module_spec is None or module_spec.origin is None:
        pytest.fail("Could not locate 'src' module.")

    src_path = pathlib.Path(module_spec.origin).parent
    project_root = src_path.parent

    return project_root


def get_python_files():
    project_root = get_project_root()
    return list(project_root.rglob("*.py"))


@pytest.mark.parametrize(
    "file_path",
    get_python_files(),
    ids=lambda f: str(f.relative_to(get_project_root())),
)
def test_style(file_path):
    result = subprocess.run(
        ["black", "--check", "--diff", str(file_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(f"Bad style - Reformat with Black.")
