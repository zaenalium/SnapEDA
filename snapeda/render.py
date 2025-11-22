from __future__ import annotations

from typing import Iterable

from rich.console import Console
from rich.table import Table

from .eda import SummarizeResult
from .io import format_paths


def _table_from_mapping(title: str, mapping: dict[str, dict[str, object]]) -> Table:
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Column", style="bold")
    if not mapping:
        table.add_row("(none)")
        return table

    keys = sorted({key for values in mapping.values() for key in values.keys()})
    for key in keys:
        table.add_column(key)

    for col, stats in mapping.items():
        row = [col]
        for key in keys:
            row.append(str(stats.get(key, "")))
        table.add_row(*row)
    return table


def _table_missingness(missingness: dict[str, float]) -> Table:
    table = Table(title="Missingness", header_style="bold magenta")
    table.add_column("Column", style="bold")
    table.add_column("Missing %")
    if not missingness:
        table.add_row("(none)", "0.0")
        return table
    for col, pct in missingness.items():
        table.add_row(col, f"{pct*100:.2f}%")
    return table


def render_text(result: SummarizeResult, *, console: Console | None = None) -> None:
    console = console or Console()

    overview = result.overview
    overview_table = Table(title="Dataset Overview", header_style="bold magenta")
    overview_table.add_column("Metric", style="bold")
    overview_table.add_column("Value")
    overview_table.add_row("Rows", f"{overview.row_count:,}")
    overview_table.add_row("Columns", str(overview.column_count))
    overview_table.add_row("Sample Rows", str(overview.sample_rows))
    overview_table.add_row("Sample Columns", str(overview.sample_columns))
    overview_table.add_row("Schema", ", ".join(f"{k}:{v}" for k, v in overview.schema.items()))

    load_table = Table(title="Files", header_style="bold magenta")
    load_table.add_column("Included")
    load_table.add_column("Skipped")
    load_table.add_row(
        format_paths(result.load_report.included) or "(none)",
        format_paths(result.load_report.skipped) or "(none)",
    )

    console.print(overview_table)
    console.print(load_table)
    console.print(_table_from_mapping("Numeric Summary", dict(result.numeric)))
    console.print(_table_from_mapping("Categorical Summary", dict(result.categorical)))
    console.print(_table_missingness(dict(result.missingness)))

    preview_table = Table(title="Sample Preview", header_style="bold magenta")
    if result.sample_preview.is_empty():
        preview_table.add_row("(empty)")
    else:
        preview_table.add_column("row")
        for col in result.sample_preview.columns:
            preview_table.add_column(col)
        for idx, row in enumerate(result.sample_preview.iter_rows()):
            preview_table.add_row(str(idx), *[str(val) for val in row])
    console.print(preview_table)
