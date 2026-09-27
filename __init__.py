from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# ── One menu root for every Code2Collapse pack ─────────────────────────────
# Every node lands under "🐺 C2C/<pack>/<family>" in the Add Node menu and the
# node library (see _c2c_menu.py). Node ids are untouched, so saved workflows
# are unaffected. Guarded: a menu placement must never cost the pack its nodes.
try:
    from ._c2c_menu import rebrand_v1 as _c2c_menu_rebrand

    _c2c_menu_rebrand(
        NODE_CLASS_MAPPINGS, "\U0001F43E Wan Animal Preprocess",
        strip=("WanAnimalPreprocess",),
        rename=None,
    )
except Exception as _c2c_menu_exc:  # noqa: BLE001
    import logging as _c2c_menu_log

    _c2c_menu_log.getLogger(__name__).warning("C2C menu root not applied: %s", _c2c_menu_exc)


# Carries only the Code2Collapse house brand (_c2c_brand.js).
WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]