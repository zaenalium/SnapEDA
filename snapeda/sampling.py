from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

import polars as pl


SamplingMode = Literal["none", "head", "tail", "random", "stratified"]


@dataclass(slots=True)
class SamplingConfig:
    mode: SamplingMode = "random"
    size: int = 5000
    fraction: Optional[float] = None
    stratify_by: Optional[str] = None
    seed: Optional[int] = 0

    @classmethod
    def from_cli(cls, args: "argparse.Namespace") -> "SamplingConfig":  # type: ignore[name-defined]
        return cls(
            mode=args.sample_mode,
            size=args.sample_size,
            fraction=args.sample_fraction,
            stratify_by=args.stratify_by,
            seed=args.seed,
        )


def apply_sampling(lf: pl.LazyFrame, config: SamplingConfig) -> pl.LazyFrame:
    if config.mode == "none":
        return lf
    if config.mode == "head":
        return lf.limit(config.size)
    if config.mode == "tail":
        return lf.tail(config.size)

    if config.mode in {"random", "stratified"}:
        sample_kwargs: dict[str, object] = {
            "with_replacement": False,
            "shuffle": True,
            "seed": config.seed,
        }
        if config.fraction is not None:
            sample_kwargs["fraction"] = config.fraction
        else:
            sample_kwargs["n"] = config.size

        if config.mode == "stratified" and config.stratify_by:
            sample_kwargs["by"] = config.stratify_by
        return lf.sample(**sample_kwargs)

    return lf
