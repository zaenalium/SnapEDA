import polars as pl
import pytest

from snapeda.eda import summarize, summarize_frame
from snapeda.sampling import SamplingConfig, normalize_sampling


def test_normalize_sampling_accepts_dict():
    cfg = normalize_sampling({"mode": "head", "size": 3, "seed": 42})

    assert isinstance(cfg, SamplingConfig)
    assert cfg.mode == "head"
    assert cfg.size == 3
    assert cfg.seed == 42


def test_summarize_frame_with_polars_dataframe():
    df = pl.DataFrame({"num": [1, 2, 3, 4], "cat": ["a", "b", "a", None]})

    result = summarize_frame(df, sample={"mode": "none"}, columns_limit=10)

    assert result.overview.row_count == 4
    assert result.overview.column_count == 2
    assert "num" in result.numeric
    assert result.numeric["num"]["min"] == pytest.approx(1.0)
    assert result.numeric["num"]["max"] == pytest.approx(4.0)
    assert result.missingness["cat"] == pytest.approx(0.25)

    rendered = result.to_text()
    assert "Dataset Overview" in rendered
    assert "Numeric Summary" in rendered


def test_summarize_directory_head_sampling(tmp_path):
    file1 = tmp_path / "part1.csv"
    file2 = tmp_path / "part2.csv"
    file1.write_text("value,cat\n1,x\n2,y\n")
    file2.write_text("value,cat\n3,y\n4,z\n")

    result = summarize(str(tmp_path), sample={"mode": "head", "size": 3})

    assert result.overview.row_count == 4
    assert len(result.load_report.included) == 2
    assert result.load_report.skipped == []
    assert result.sample_preview.height == 3
    assert "value" in result.numeric
