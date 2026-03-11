from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LiabilityCalculationResult:
    total_amount: float
    is_candidate_for_sharing: bool
    shared_amount: float


__all__ = ["LiabilityCalculationResult"]

