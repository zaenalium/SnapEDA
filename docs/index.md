# SnapEDA documentation

SnapEDA provides quick, text-first exploratory data analysis (EDA) with a Polars backend.
It focuses on fast startup, minimal memory use, and helpful defaults so you can inspect
single files or directories of structured data with little configuration.

## Highlights
- Polars-first lazy loading for CSV/TSV, Parquet, and IPC/Feather
- Directory-aware discovery with glob patterns and diagonal concatenation
- Sampling policies (none, head, tail, random, stratified) to keep work fast
- Text rendering powered by Rich for clear summaries in the terminal
- Works with on-disk files or in-memory Polars/pandas DataFrames

## Installation
Install SnapEDA from a local checkout:

```bash
pip install -e .
```

To build the docs locally, install MkDocs (no theme extras required):

```bash
pip install mkdocs
mkdocs serve
```

## What you get
SnapEDA returns a `SummarizeResult` dataclass containing:
- **overview**: row/column counts, sample dimensions, and schema
- **numeric**: per-column stats such as mean, std, min/max, and quantiles
- **categorical**: distinct counts, entropy, and top frequencies
- **missingness**: per-column missing fraction
- **sample_preview**: first 10 rows from the sampled frame
- **load_report**: which files were included or skipped during ingestion

Use `snapeda.render.render_text` to print the result as formatted tables in your terminal,
or call `result.to_text()` to capture the same output as a string.
