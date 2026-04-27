from __future__ import annotations

from ._core_payload import load_into_globals as _load_into_globals

_load_into_globals(globals(), __name__, __file__)

del _load_into_globals
