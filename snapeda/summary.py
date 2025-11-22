from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping

import polars as pl


@dataclass(slots=True)
class DatasetOverview:
    row_count: int
    column_count: int
    schema: Mapping[str, str]
    sample_rows: int
    sample_columns: int


@dataclass(slots=True)
class SummaryBundle:
    overview: DatasetOverview
    numeric: Mapping[str, Mapping[str, float | int | str]]
    categorical: Mapping[str, Mapping[str, object]]
    missingness: Mapping[str, float]


NUMERIC_LIMIT = 50


def summarize_dataset(lf: pl.LazyFrame, sample_df: pl.DataFrame) -> DatasetOverview:
    row_count = int(lf.select(pl.len()).collect().item())
    schema = {k: str(v) for k, v in lf.schema.items()}
    return DatasetOverview(
        row_count=row_count,
        column_count=len(schema),
        schema=schema,
        sample_rows=sample_df.height,
        sample_columns=sample_df.width,
    )


def _numeric_columns(df: pl.DataFrame) -> list[str]:
    numeric_cols: list[str] = []
    for name, dtype in df.schema.items():
        if pl.datatypes.is_numeric(dtype):
            numeric_cols.append(name)
    return numeric_cols


def summarize_numeric(df: pl.DataFrame, *, columns_limit: int = 25) -> Dict[str, Dict[str, float | int | str]]:
    numeric_cols = _numeric_columns(df)[:columns_limit]
    summary: Dict[str, Dict[str, float | int | str]] = {}
    for col in numeric_cols:
        series = df.get_column(col)
        if series.is_empty():
            continue
        summary[col] = {
            "min": float(series.min()),
            "max": float(series.max()),
            "mean": float(series.mean()),
            "std": float(series.std()),
            "p25": float(series.quantile(0.25)),
            "p50": float(series.median()),
            "p75": float(series.quantile(0.75)),
            "nulls": int(series.null_count()),
            "unique": int(series.n_unique()),
        }
    return summary


def _categorical_columns(df: pl.DataFrame) -> list[str]:
    categorical_cols: list[str] = []
    for name, dtype in df.schema.items():
        if dtype in (pl.Utf8, pl.Categorical):
            categorical_cols.append(name)
    return categorical_cols


def summarize_categorical(df: pl.DataFrame, *, columns_limit: int = 25) -> Dict[str, Dict[str, object]]:
    cat_cols = _categorical_columns(df)[:columns_limit]
    summary: Dict[str, Dict[str, object]] = {}
    for col in cat_cols:
        series = df.get_column(col)
        if series.is_empty():
            continue
        vc = series.value_counts().sort("count", descending=True).head(5)
        top_values = [(str(row[0]), int(row[1])) for row in vc.iter_rows()] if vc.height else []
        summary[col] = {
            "unique": int(series.n_unique()),
            "mode": top_values[0][0] if top_values else None,
            "mode_freq": top_values[0][1] if top_values else 0,
            "top_values": top_values,
            "nulls": int(series.null_count()),
        }
    return summary


def summarize_missingness(df: pl.DataFrame) -> Dict[str, float]:
    if df.height == 0:
        return {}
    null_counts = df.null_count()
    return {col: float(null_counts[col][0]) / float(df.height) for col in df.columns}
