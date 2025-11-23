import unittest

import polars as pl

from snapeda.cli import _build_parser
from snapeda.sampling import SamplingConfig, apply_sampling


class SamplingValidationTests(unittest.TestCase):
    def test_stratified_sampling_requires_column(self) -> None:
        lf = pl.LazyFrame({"group": ["a", "b", "c"]})
        config = SamplingConfig(mode="stratified", size=2, stratify_by=None)

        with self.assertRaises(ValueError):
            apply_sampling(lf, config)

    def test_cli_config_requires_stratify_by(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["data.csv", "--sample-mode", "stratified"])

        with self.assertRaises(ValueError):
            SamplingConfig.from_cli(args)


if __name__ == "__main__":
    unittest.main()
