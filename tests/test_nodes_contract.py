"""Node contract tests — IS_CHANGED, IMAGE validation, inference_mode."""
from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


_PKG = "wan_animal_pack"


def _load_pack():
    """Load the pack the way ComfyUI does - as a package, so nodes.py's
    relative imports resolve and __init__.py's registration runs."""
    if _PKG in sys.modules:
        return sys.modules[_PKG]
    spec = importlib.util.spec_from_file_location(
        _PKG, ROOT / "__init__.py", submodule_search_locations=[str(ROOT)])
    assert spec and spec.loader
    pkg = importlib.util.module_from_spec(spec)
    sys.modules[_PKG] = pkg
    try:
        spec.loader.exec_module(pkg)
    except ModuleNotFoundError as exc:
        sys.modules.pop(_PKG, None)
        pytest.skip(f"nodes.py dependencies unavailable (set COMFYUI_PATH): {exc}")
    return pkg


def _load_nodes_module():
    _load_pack()
    return sys.modules[f"{_PKG}.nodes"]


@pytest.mark.skipif(
    importlib.util.find_spec("torch") is None,
    reason="torch not installed in this interpreter",
)
def test_every_node_sits_under_the_code2collapse_menu_root():
    pack = _load_pack()
    assert pack.NODE_CLASS_MAPPINGS
    for name, cls in pack.NODE_CLASS_MAPPINGS.items():
        assert cls.CATEGORY.startswith("\U0001F43A C2C/\U0001F43E Wan Animal Preprocess"), (
            f"{name}: {cls.CATEGORY}")
    assert pack.WEB_DIRECTORY == "./web"
    assert (ROOT / "web" / "_c2c_brand.js").is_file()


@pytest.mark.skipif(
    importlib.util.find_spec("torch") is None,
    reason="torch not installed in this interpreter",
)
def test_all_nodes_define_is_changed():
    nodes = _load_nodes_module()
    for name, cls in nodes.NODE_CLASS_MAPPINGS.items():
        assert hasattr(cls, "IS_CHANGED"), f"{name} missing IS_CHANGED"
        out = cls.IS_CHANGED()
        assert isinstance(out, str), f"{name}.IS_CHANGED must return str"
        assert out == out, f"{name}.IS_CHANGED returned NaN"


@pytest.mark.skipif(
    importlib.util.find_spec("torch") is None,
    reason="torch not installed in this interpreter",
)
def test_image_nodes_reject_bad_shape():
    import torch

    nodes = _load_nodes_module()
    bad = torch.zeros(3, 64, 64)

    for cls_name in ("AnimalPoseAndDetection", "AnimalPoseDetectionOneToAllAnimation"):
        cls = nodes.NODE_CLASS_MAPPINGS[cls_name]
        extra = {}
        if cls_name == "AnimalPoseDetectionOneToAllAnimation":
            extra = {"align_to": "none", "draw_head": "full"}
        with pytest.raises(ValueError, match="IMAGE"):
            cls().process(
                model={"yolo": None, "vitpose": None, "dataset": "ap10k"},
                images=bad,
                width=832,
                height=480,
                **extra,
            )

    with pytest.raises(ValueError, match="IMAGE"):
        nodes.AnimalPoseAndDetection().process(
            model={"yolo": None, "vitpose": None, "dataset": "ap10k"},
            images=torch.zeros(1, 64, 64, 3),
            width=832,
            height=480,
            retarget_image=torch.zeros(64, 64, 3),
        )


@pytest.mark.skipif(
    importlib.util.find_spec("torch") is None,
    reason="torch not installed in this interpreter",
)
def test_process_methods_use_inference_mode():
    nodes = _load_nodes_module()
    for name, cls in nodes.NODE_CLASS_MAPPINGS.items():
        fn = getattr(cls, cls.FUNCTION)
        src = inspect.getsource(fn)
        assert "inference_mode" in src, f"{name}.{cls.FUNCTION} must use torch.inference_mode()"
