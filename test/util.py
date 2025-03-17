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
