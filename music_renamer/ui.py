from __future__ import annotations

import base64
import lzma
from pathlib import Path

_payload_dir = Path(__file__).with_name("_ui_parts")
_encoded = "".join(
    (_payload_dir / f"part{index:02d}.txt").read_text(encoding="utf-8")
    for index in range(1, 6)
)
_source = lzma.decompress(base64.b64decode(_encoded)).decode("utf-8")
exec(compile(_source, __file__, "exec"), globals())

del Path, _payload_dir, _encoded, _source, base64, lzma
