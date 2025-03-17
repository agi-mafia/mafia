import importlib.util
import pathlib

import pytest


def get_project_root():
    module_spec = importlib.util.find_spec("src")
    if module_spec is None or module_spec.origin is None:
        pytest.fail("Could not locate 'src' module.")

    src_path = pathlib.Path(module_spec.origin).parent
    project_root = src_path.parent

    return project_root


PROJECT_ROOT = get_project_root()


def get_python_files_absolute():
    return list(PROJECT_ROOT.rglob("*.py"))


PYTHON_FILES_ABSOLUTE = get_python_files_absolute()


def get_python_files_relative():
    return [
        str(python_file.relative_to(PROJECT_ROOT))
        for python_file in PYTHON_FILES_ABSOLUTE
    ]


PYTHON_FILES_RELATIVE = get_python_files_relative()
