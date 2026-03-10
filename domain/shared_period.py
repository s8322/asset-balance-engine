from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class SharedPeriod:
    start: date
    end: date

    def __post_init__(self) -> None:
        if self.end < self.start:
            raise ValueError("end date must be greater than or equal to start date")

    def days(self) -> int:
        return (self.end - self.start).days + 1

    def overlap(self, other: "SharedPeriod") -> "SharedPeriod | None":
        overlap_start = max(self.start, other.start)
        overlap_end = min(self.end, other.end)

        if overlap_end < overlap_start:
            return None

        return SharedPeriod(start=overlap_start, end=overlap_end)

    def overlap_days(self, other: "SharedPeriod") -> int:
        overlap_period = self.overlap(other)
        if overlap_period is None:
            return 0
        return overlap_period.days()


__all__ = ["SharedPeriod"]

