"""Root conftest - let `pytest` run from the repo root.

The root __init__.py is ComfyUI's entry point and uses a relative import
(`from .nodes import ...`). With no pytest config at the root, pytest treats
the repo root as a package and imports that file bare, as a module named
"__init__", where a relative import cannot work - so every test errored at
collection (41 errors, hidden in CI by `pytest -q || true`).

Same fix as ComfyUI-CustomNodePacks, narrowed to the one directory: the root
package's setup tolerates that import. The tests load the pack properly, as a
package (tests/test_nodes_contract.py), so nothing is lost.
"""

from pathlib import Path

from _pytest.python import Package

ROOT = Path(__file__).resolve().parent

# A standalone script (its own `test(name, fn)` runner, not pytest):
#     python test_animal_pose.py
collect_ignore = ["test_animal_pose.py"]

_original_setup = Package.setup


def _root_tolerant_setup(self):
    try:
        _original_setup(self)
    except Exception:
        # pytest wraps the failed bare import in its own CollectError, so the
        # type says nothing - the directory does. Anywhere else, fail as usual.
        if Path(self.path).resolve() != ROOT:
            raise


Package.setup = _root_tolerant_setup
