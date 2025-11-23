import polars as pl
import pytest

from snapeda.sampling import SamplingConfig, apply_sampling, normalize_sampling


def test_normalize_sampling_rejects_unknown_mode():
    config = SamplingConfig(mode="bogus")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="Unknown sampling mode"):
        normalize_sampling(config)


def test_apply_sampling_validates_unknown_mode_before_plan():
    lf = pl.DataFrame({"x": [1, 2]}).lazy()
    config = SamplingConfig(mode="invalid")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="Unknown sampling mode"):
        apply_sampling(lf, config)


def test_normalize_sampling_rejects_non_positive_size():
    config = SamplingConfig(mode="head", size=0)
    with pytest.raises(ValueError, match="positive integer"):
        normalize_sampling(config)


def test_normalize_sampling_rejects_fraction_out_of_range():
    with pytest.raises(ValueError, match=r"within \(0, 1\]"):
        normalize_sampling(SamplingConfig(mode="random", fraction=0))

    with pytest.raises(ValueError, match=r"within \(0, 1\]"):
        normalize_sampling(SamplingConfig(mode="random", fraction=1.5))
