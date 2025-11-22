from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

import polars as pl

SUPPORTED_EXTENSIONS = {
    ".csv": "csv",
    ".tsv": "csv",
    ".parquet": "parquet",
    ".pq": "parquet",
    ".ipc": "ipc",
    ".feather": "ipc",
}


@dataclass(slots=True)
class LoadReport:
    included: List[Path]
    skipped: List[Path]
    reason: str | None = None


class LoaderError(RuntimeError):
    """Raised when no usable files were discovered."""


def discover_files(path: Path, pattern: str) -> Sequence[Path]:
    if path.is_file():
        return [path]
    files = sorted(
        p for p in path.glob(pattern) if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    return files


def _scan_file(path: Path) -> pl.LazyFrame | None:
    suffix = path.suffix.lower()
    kind = SUPPORTED_EXTENSIONS.get(suffix)
    if kind == "csv":
        return pl.scan_csv(path, infer_schema_length=200)
    if kind == "parquet":
        return pl.scan_parquet(path)
    if kind == "ipc":
        return pl.scan_ipc(path)
    return None


def load_lazy_frame(path: str | Path, pattern: str = "*") -> tuple[pl.LazyFrame, LoadReport]:
    base = Path(path).expanduser().resolve()
    files = discover_files(base, pattern)
    included: list[Path] = []
    skipped: list[Path] = []
    lazy_parts: list[pl.LazyFrame] = []

    for file in files:
        lf = _scan_file(file)
        if lf is None:
            skipped.append(file)
            continue
        included.append(file)
        lazy_parts.append(lf)

    if not lazy_parts:
        raise LoaderError(f"No supported files found in {base}")

    combined = lazy_parts[0] if len(lazy_parts) == 1 else pl.concat(lazy_parts, how="diagonal")
    return combined, LoadReport(included=included, skipped=skipped)


def format_paths(paths: Iterable[Path]) -> str:
    return ", ".join(str(p) for p in paths)
