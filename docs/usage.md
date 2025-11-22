# Usage

SnapEDA offers a Python API and a CLI that share the same pipeline. Choose a sampling
strategy to keep computations snappy, and render the result as rich text tables.

## Python API
```python
import snapeda as se
from snapeda import SamplingConfig
from snapeda.render import render_text

# File or directory path (glob pattern applies when pointing at a folder)
result = se.summarize(
    "data/",  # file, directory, or glob root
    sample=SamplingConfig(mode="random", size=5000, seed=0),
    pattern="*.parquet",
    columns_limit=25,
)
render_text(result)

# In-memory Polars DataFrame
# df_polars = pl.DataFrame(...)
polar_result = se.summarize_frame(df_polars)

# In-memory pandas DataFrame
# df_pandas = pd.DataFrame(...)
pandas_result = se.summarize_frame(df_pandas, sample=SamplingConfig(mode="head", size=100))
```

Key options:
- `pattern`: Glob pattern for directory discovery (defaults to `*`).
- `columns_limit`: Truncate numeric/categorical summaries to the first N columns.
- `sample`: `SamplingConfig` controlling mode, size/fraction, stratification, and seed.

## CLI
The CLI mirrors the Python API. All sampling modes are available, and directory loading
uses the same glob pattern handling.

```bash
python -m snapeda data/ --pattern "*.parquet" \
  --sample-mode random --sample-size 5000 --seed 0 \
  --columns-limit 25
```

Flags:
- `source` (positional): file or directory path.
- `--pattern`: glob used when `source` is a directory.
- `--sample-mode`: `none`, `head`, `tail`, `random`, or `stratified`.
- `--sample-size` / `--sample-fraction`: specify absolute or fractional sampling.
- `--stratify-by`: column for stratified sampling.
- `--seed`: random seed for reproducible sampling.
- `--columns-limit`: maximum columns to summarize.

The CLI renders text tables directly to stdout using Rich.
