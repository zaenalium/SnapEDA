# SnapEDA

A simple, fast, and memory-efficient Auto EDA utility built on Polars with text output.

## Features
- **Polars-first** lazy ingestion for CSV, TSV, Parquet, IPC/Feather
- **Directory-aware** loading with glob patterns and lazy concatenation
- **Sampling policies**: head, tail, random, or stratified
- **Text summaries** rendered with Rich
- **CLI and Python API** entrypoints

## Quickstart

### Python API
```python
import snapeda as se
from snapeda import SamplingConfig

result = se.summarize(
    "data/",  # file or directory
    sample=SamplingConfig(mode="random", size=5000, seed=0),
    pattern="*.parquet",  # optional when pointing at a folder
)

# In-memory Polars or pandas DataFrame
# df_polars = pl.DataFrame(...)
# df_pandas = pd.DataFrame(...)
# pip install snapeda[pandas]  # needed for pandas inputs
result_from_df = se.summarize_frame(df_polars)
```

### CLI
```
python -m snapeda data/ --pattern "*.parquet" --sample-mode random --sample-size 5000
```

## Sampling modes
- `head`: take the first N rows
- `tail`: take the last N rows
- `random`: uniform sampling across the dataset
- `stratified`: stratified sampling by a column (`--stratify-by`, required when this mode is used)
- `none`: operate on the full dataset (may be slower)

## Documentation
Additional guides and examples live in the MkDocs site under `docs/`. Build locally with:

```bash
pip install mkdocs
mkdocs serve
```

- A Jupytext-friendly tutorial is available at `docs/tutorial.md` and opens as a notebook in
  JupyterLab or VS Code without creating a separate `.ipynb` file. Pair it with a notebook via:

```bash
jupytext --set-formats md,ipynb docs/tutorial.md
```
