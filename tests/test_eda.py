from __future__ import annotations

import builtins

import polars as pl
import pytest

from snapeda.eda import _lazy_from_frame


def test_lazy_from_frame_missing_pandas(monkeypatch):
    """Ensure a helpful error is raised when pandas is unavailable."""

    DataFrame = type("DataFrame", (), {"__module__": "pandas.core.frame"})
    fake_frame = DataFrame()

    real_import = builtins.__import__

    def raise_for_pandas(name, *args, **kwargs):
        if name.startswith("pandas"):
            raise ModuleNotFoundError("No module named 'pandas'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", raise_for_pandas)

    with pytest.raises(ImportError, match=r"snapeda\[pandas\]"):
        _lazy_from_frame(fake_frame)


def test_lazy_from_frame_with_pandas():
    """Conversion succeeds when pandas is installed."""

    pd = pytest.importorskip("pandas")
    frame = pd.DataFrame({"a": [1, 2]})

    result = _lazy_from_frame(frame)

    assert isinstance(result, pl.LazyFrame)
    assert result.collect().to_dict(as_series=False) == {"a": [1, 2]}
