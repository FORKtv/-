from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ScanOptions:
    naming_rule: str = "custom"
    include_subfolders: bool = True
    auto_clean_illegal_chars: bool = True
    naming_pattern: str = "[标题] - [艺术家]"
    keep_extension: bool = True
    trim_whitespace: bool = True
    auto_number_duplicates: bool = True
    skip_missing_tags: bool = False


@dataclass(slots=True)
class AudioMetadata:
    title: str = ""
    artist: str = ""
    album: str = ""
    track_number: str = ""
    year: str = ""
    read_error: str = ""
    title_garbled: bool = False

    def has_any(self) -> bool:
        return bool(self.title or self.artist or self.album or self.track_number or self.year)


@dataclass(slots=True)
class PreviewEntry:
    index: int
    original_path: Path
    current_path: Path
    original_name: str
    extension: str
    title: str = ""
    artist: str = ""
    album: str = ""
    track_number: str = ""
    year: str = ""
    read_error: str = ""
    title_garbled: bool = False
    generated_name: str = ""
    new_name: str = ""
    status_code: str = "unscanned"
    note: str = ""
    processed_at: str = ""
    manual_new_name: str = ""
    is_manual_name: bool = False
    selected: bool = True
    manual_skip: bool = False
    last_target_path: str = ""

    @property
    def target_path(self) -> Path | None:
        if not self.new_name:
            return None
        return self.current_path.with_name(self.new_name)

    @property
    def can_rename(self) -> bool:
        return self.selected and self.status_code == "renamable"

    @property
    def format_label(self) -> str:
        return self.extension.lstrip(".").upper()

    @property
    def searchable_text(self) -> str:
        return " ".join(
            [
                self.original_name,
                self.title,
                self.artist,
                self.album,
                self.year,
                self.new_name,
                self.note,
                self.format_label,
            ]
        ).lower()

    @property
    def existing_path(self) -> Path:
        if self.current_path.exists():
            return self.current_path
        target = self.target_path
        if target and target.exists():
            return target
        return self.current_path


@dataclass(frozen=True, slots=True)
class CompletedAction:
    old_path: Path
    new_path: Path
    processed_at: str
