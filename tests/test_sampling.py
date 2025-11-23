from pathlib import Path
import sys

import polars as pl
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from snapeda.sampling import SamplingConfig, apply_sampling


def test_stratified_sampling_missing_column_raises_value_error():
    lf = pl.DataFrame({"value": [1, 2, 3]}).lazy()
    config = SamplingConfig(mode="stratified", stratify_by="group")

    with pytest.raises(ValueError, match="Column 'group' is required for stratified sampling"):
        apply_sampling(lf, config)
