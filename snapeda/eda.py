from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, TYPE_CHECKING

import polars as pl

from .io import LoadReport, load_lazy_frame
from .sampling import SamplingConfig, apply_sampling
from .summary import (
    DatasetOverview,
    summarize_categorical,
    summarize_dataset,
    summarize_missingness,
    summarize_numeric,
)


@dataclass(slots=True)
class SummarizeOptions:
    pattern: str = "*"
    columns_limit: int = 25


@dataclass(slots=True)
class SummarizeResult:
    overview: DatasetOverview
    numeric: Mapping[str, Mapping[str, float | int | str]]
    categorical: Mapping[str, Mapping[str, object]]
    missingness: Mapping[str, float]
    sample_preview: pl.DataFrame
    load_report: LoadReport


if TYPE_CHECKING:  # pragma: no cover
    import pandas as pd


DEFAULT_SAMPLE = SamplingConfig(mode="random", size=5000, seed=0)


def _lazy_from_frame(frame: pl.DataFrame | "pd.DataFrame") -> pl.LazyFrame:
    if isinstance(frame, pl.DataFrame):
        return frame.lazy()

    # Lightweight pandas detection without importing the module eagerly.
    if frame.__class__.__name__ == "DataFrame" and frame.__class__.__module__.startswith("pandas"):
        return pl.from_pandas(frame).lazy()

    raise TypeError("frame must be a Polars or pandas DataFrame")


def summarize(
    source: str,
    sample: SamplingConfig | None = None,
    *,
    pattern: str = "*",
    columns_limit: int = 25,
) -> SummarizeResult:
    sample_cfg = sample or DEFAULT_SAMPLE
    lf, load_report = load_lazy_frame(source, pattern=pattern)

    sampled_lf = apply_sampling(lf, sample_cfg)
    sample_df = sampled_lf.collect()

    overview = summarize_dataset(lf, sample_df)
    numeric = summarize_numeric(sample_df, columns_limit=columns_limit)
    categorical = summarize_categorical(sample_df, columns_limit=columns_limit)
    missingness = summarize_missingness(sample_df)

    return SummarizeResult(
        overview=overview,
        numeric=numeric,
        categorical=categorical,
        missingness=missingness,
        sample_preview=sample_df.head(10),
        load_report=load_report,
    )


def summarize_frame(
    frame: pl.DataFrame | "pd.DataFrame",
    sample: SamplingConfig | None = None,
    *,
    columns_limit: int = 25,
) -> SummarizeResult:
    sample_cfg = sample or DEFAULT_SAMPLE

    lf = _lazy_from_frame(frame)
    sampled_lf = apply_sampling(lf, sample_cfg)
    sample_df = sampled_lf.collect()

    overview = summarize_dataset(lf, sample_df)
    numeric = summarize_numeric(sample_df, columns_limit=columns_limit)
    categorical = summarize_categorical(sample_df, columns_limit=columns_limit)
    missingness = summarize_missingness(sample_df)

    return SummarizeResult(
        overview=overview,
        numeric=numeric,
        categorical=categorical,
        missingness=missingness,
        sample_preview=sample_df.head(10),
        load_report=LoadReport(included=[], skipped=[], reason="in-memory frame"),
    )
