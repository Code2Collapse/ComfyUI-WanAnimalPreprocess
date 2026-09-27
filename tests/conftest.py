"""Make ComfyUI's own modules importable when the suite runs outside ComfyUI.

nodes.py imports `folder_paths` and `comfy`, which only exist inside a ComfyUI
checkout. Without one the node-contract tests used to skip every time - on
every machine, including CI - so the nodes themselves were never tested.

So: find a ComfyUI checkout and put it on sys.path. COMFYUI_PATH wins when
set; otherwise the usual places relative to this pack are tried. With none
found, the tests that need it still skip, and say why.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
WORKSPACE = PACK.parent

#: Where a ComfyUI checkout usually sits relative to a custom-node pack: the
#: Windows dev workspace (junctioned into the portable install), a checkout
#: beside the workspace, and a pack living directly in custom_nodes/.
_CANDIDATES = [
    WORKSPACE.parent / "ComfyUI_windows_portable" / "ComfyUI",
    WORKSPACE / "ComfyUI",
    PACK.parent.parent,
]
if os.environ.get("COMFYUI_PATH"):
    _CANDIDATES.insert(0, Path(os.environ["COMFYUI_PATH"]))


def _find_comfy() -> Path | None:
    for cand in _CANDIDATES:
        try:
            if (cand / "folder_paths.py").is_file() and (cand / "comfy").is_dir():
                return cand
        except OSError:
            continue
    return None


COMFY_ROOT = _find_comfy()
if COMFY_ROOT is not None and str(COMFY_ROOT) not in sys.path:
    sys.path.insert(0, str(COMFY_ROOT))
