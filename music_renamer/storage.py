from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any


APP_FOLDER_NAME = "MusicTitleRenamer"
DEFAULT_CONFIG = {
    "default_naming_pattern": "[标题] - [艺术家]",
    "keep_extension": True,
    "auto_clean_illegal_chars": True,
    "trim_whitespace": True,
    "auto_number_duplicates": True,
    "skip_missing_tags": False,
    "include_subfolders": False,
    "log_dir": "",
    "theme_mode": "light",
}


def get_app_data_dir() -> Path:
    base_dir = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming")
    app_dir = base_dir / APP_FOLDER_NAME
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


def get_config_path() -> Path:
    return get_app_data_dir() / "config.json"


def get_history_path() -> Path:
    return get_app_data_dir() / "history.json"


def load_config() -> tuple[dict[str, Any], bool]:
    path = get_config_path()
    default_copy = deepcopy(DEFAULT_CONFIG)
    if not path.exists():
        return default_copy, False

    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError("配置内容不是对象")
    except Exception:
        return default_copy, True

    merged = default_copy
    merged.update({key: value for key, value in data.items() if key in merged})
    return merged, False


def save_config(config: dict[str, Any]) -> Path:
    path = get_config_path()
    path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8-sig")
    return path


def load_history() -> list[dict[str, Any]]:
    path = get_history_path()
    if not path.exists():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return []

    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def save_history(records: list[dict[str, Any]]) -> Path:
    path = get_history_path()
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8-sig")
    return path


def clear_history() -> Path:
    return save_history([])


def resolve_log_dir(config: dict[str, Any], fallback_root: Path) -> Path:
    raw_value = str(config.get("log_dir", "") or "").strip()
    if raw_value:
        log_dir = Path(raw_value)
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir

    log_dir = fallback_root / "rename_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir
