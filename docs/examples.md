# Examples

These scenarios illustrate how to combine sampling, directory loading, and different
backends when running EDA with SnapEDA.

## Summarize a directory of Parquet files
```python
from snapeda import SamplingConfig, summarize
from snapeda.render import render_text

result = summarize(
    "data/events/",            # folder containing multiple Parquet files
    pattern="*.parquet",       # only include Parquet data
    sample=SamplingConfig(mode="random", size=10_000, seed=42),
    columns_limit=20,
)
render_text(result)
```
This discovers all Parquet files in the directory, concatenates them lazily, samples
10,000 rows across the combined dataset, and renders numeric/categorical summaries
with a sample preview.

## Stratified sampling on an in-memory pandas DataFrame
```python
import pandas as pd
from snapeda import SamplingConfig, summarize_frame

raw = pd.read_parquet("data/customers.parquet")
result = summarize_frame(
    raw,
    sample=SamplingConfig(mode="stratified", size=5_000, stratify_by="country", seed=11),
)
```
The dataframe is converted to Polars under the hood, stratified on the `country` column,
and summarized using the same pipeline as on-disk data.

## Turn off sampling for small CSVs via CLI
```bash
python -m snapeda data/small.csv --sample-mode none --columns-limit 50
```
When sampling is disabled, SnapEDA operates on the full dataset; use this for datasets
that fit comfortably in memory.

## Limit summaries to specific columns
If you only want to include the first few columns in the numeric/categorical tables,
set `columns_limit`:

```python
from snapeda import SamplingConfig, summarize

result = summarize(
    "data/wide_dataset.parquet",
    sample=SamplingConfig(mode="head", size=1_000),
    columns_limit=10,
)
```
Only the first 10 columns in the sampled frame are included in the per-column summaries,
while the overview and preview still reflect the full schema.
