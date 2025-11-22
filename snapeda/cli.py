from __future__ import annotations

import argparse

from .eda import summarize
from .render import render_text
from .sampling import SamplingConfig


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SnapEDA - quick text EDA for structured data")
    parser.add_argument("source", help="File or directory containing data files")
    parser.add_argument("--pattern", default="*", help="Glob pattern for directory loading")
    parser.add_argument(
        "--sample-mode",
        default="random",
        choices=["none", "head", "tail", "random", "stratified"],
        help="Sampling strategy",
    )
    parser.add_argument("--sample-size", type=int, default=5000, help="Number of rows to sample")
    parser.add_argument("--sample-fraction", type=float, default=None, help="Fractional sample instead of size")
    parser.add_argument("--stratify-by", default=None, help="Column to stratify sampling on")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for sampling")
    parser.add_argument("--columns-limit", type=int, default=25, help="Maximum columns to summarize")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    sample_cfg = SamplingConfig.from_cli(args)

    result = summarize(
        args.source,
        sample=sample_cfg,
        pattern=args.pattern,
        columns_limit=args.columns_limit,
    )
    render_text(result)


if __name__ == "__main__":
    main()
