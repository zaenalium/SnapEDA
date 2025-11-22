"""SnapEDA - simple, fast, memory-efficient Auto EDA built on Polars."""

from .eda import summarize, summarize_frame
from .sampling import SamplingConfig

__all__ = ["summarize", "summarize_frame", "SamplingConfig"]
