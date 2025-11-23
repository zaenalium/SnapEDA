from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

import polars as pl


SamplingMode = Literal["none", "head", "tail", "random", "stratified"]
_ALLOWED_MODES = {"none", "head", "tail", "random", "stratified"}


@dataclass(slots=True)
class SamplingConfig:
    mode: SamplingMode = "random"
    size: int = 5000
    fraction: Optional[float] = None
    stratify_by: Optional[str] = None
    seed: Optional[int] = 0

    @classmethod
    def from_cli(cls, args: "argparse.Namespace") -> "SamplingConfig":  # type: ignore[name-defined]
        if args.sample_mode == "stratified" and not args.stratify_by:
            raise ValueError("Stratified sampling requires --stratify-by to be set.")

        return cls(
            mode=args.sample_mode,
            size=args.sample_size,
            fraction=args.sample_fraction,
            stratify_by=args.stratify_by,
            seed=args.seed,
        )


def normalize_sampling(config: SamplingConfig) -> SamplingConfig:
    if config.mode not in _ALLOWED_MODES:
        raise ValueError(
            f"Unknown sampling mode {config.mode!r}. Allowed modes: {sorted(_ALLOWED_MODES)}"
        )

    if config.size <= 0:
        raise ValueError("sample size must be a positive integer")

    if config.fraction is not None and (config.fraction <= 0 or config.fraction > 1):
        raise ValueError("sample fraction must be within (0, 1]")

    return config


def apply_sampling(lf: pl.LazyFrame, config: SamplingConfig) -> pl.LazyFrame:
    config = normalize_sampling(config)

    if config.mode == "none":
        return lf
    if config.mode == "head":
        return lf.limit(config.size)
    if config.mode == "tail":
        return lf.tail(config.size)

    if config.mode in {"random", "stratified"}:
        if config.mode == "stratified" and not config.stratify_by:
            raise ValueError("Stratified sampling requires a 'stratify_by' column to be set.")

        sample_kwargs: dict[str, object] = {
            "with_replacement": False,
            "shuffle": True,
            "seed": config.seed,
        }
        if config.fraction is not None:
            sample_kwargs["fraction"] = config.fraction
        else:
            sample_kwargs["n"] = config.size

        if config.mode == "stratified":
            if not config.stratify_by:
                msg = "Stratified sampling requires a 'stratify_by' column name."
                raise ValueError(msg)

            schema = lf.collect_schema()
            if config.stratify_by not in schema:
                available_columns = ", ".join(schema.keys())
                msg = (
                    f"Column '{config.stratify_by}' is required for stratified sampling "
                    f"but was not found in the LazyFrame schema. Available columns: {available_columns}"
                )
                raise ValueError(msg)

            sample_kwargs["by"] = config.stratify_by

        return lf.sample(**sample_kwargs)

    return lf
