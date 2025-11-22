---
title: "SnapEDA Jupytext Tutorial"
jupytext:
  formats: md
  text_representation:
    extension: .md
    format_name: markdown
    format_version: 1.3
    jupytext_version: 1.16
kernelspec:
  name: python3
  display_name: Python 3
---

Welcome to the SnapEDA tutorial in **Jupytext** format. You can open this file as a
notebook in JupyterLab or VS Code without storing an additional `.ipynb` file.

## Prerequisites

```bash
pip install snapeda polars rich jupytext
```

If you prefer to pair this markdown file with a notebook, run:

```bash
jupytext --set-formats md,ipynb docs/tutorial.md
```

## 1. Create or load a dataframe

```python
import polars as pl
from snapeda import summarize_frame

# Build a small demo frame
customers = pl.DataFrame(
    {
        "customer_id": [1, 2, 3, 4, 5],
        "city": ["NYC", "NYC", "SF", "LA", "LA"],
        "spend": [120.5, 80.0, 200.0, 60.0, 95.0],
        "joined": pl.date_range("2024-01-01", "2024-01-05", "1d"),
    }
)
```

## 2. Run the EDA pipeline on an in-memory frame

```python
summary = summarize_frame(customers, sample={"mode": "random", "size": 3})
print(summary.render_text())
```

The sampler respects existing options like head/tail, random, or stratified sampling
without loading the full dataset into memory when used with lazy frames.

## 3. Save and reuse the summary

```python
# Access any section of the summary object
print(summary.dataset)
print(summary.numeric)

# Export text to a report file
with open("report.txt", "w") as fp:
    fp.write(summary.render_text())
```

## 4. Working with multiple files in a folder

Use the same sampling and summarization pipeline against a directory of CSV/Parquet
files. SnapEDA will lazily scan and concatenate compatible schemas.

```python
from snapeda import summarize

folder_report = summarize("./data/", sample={"mode": "head", "size": 100})
print(folder_report.render_text())
```

## 5. Sync the notebook pairing (optional)

After editing the markdown in Jupytext, regenerate the paired notebook for sharing:

```bash
jupytext --sync docs/tutorial.md
```

You can then open the synchronized `docs/tutorial.ipynb` in Jupyter or export it to
HTML/PDF via your notebook environment.
