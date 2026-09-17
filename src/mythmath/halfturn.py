"""Exact half-turn analysis for paired even-length cyclic sequences."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence


@dataclass(frozen=True)
class HalfTurnResult:
    length: int
    half_period: int
    x_pair_sum: Fraction
    y_pair_sum: Fraction
    center_x: Fraction
    center_y: Fraction
    exact: bool


def _as_fraction(value: int | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def analyze_half_turn(
    x: Sequence[int | Fraction],
    y: Sequence[int | Fraction],
) -> HalfTurnResult:
    """Test whether opposite points of an even cycle are related by a half-turn.

    For an even cycle of length ``n``, exactness means that there are constants
    ``sx`` and ``sy`` such that for every ``m``::

        x[m+n/2] = sx - x[m]
        y[m+n/2] = sy - y[m]

    Equivalently, after centering at ``(sx/2, sy/2)``, the second half of the
    cycle is the negative of the first half.
    """

    if len(x) != len(y):
        raise ValueError("x and y must have equal length")
    if len(x) == 0 or len(x) % 2:
        raise ValueError("cycle length must be non-zero and even")

    xf = tuple(_as_fraction(v) for v in x)
    yf = tuple(_as_fraction(v) for v in y)
    half = len(xf) // 2

    sx = xf[0] + xf[half]
    sy = yf[0] + yf[half]
    exact = all(
        xf[m] + xf[m + half] == sx and yf[m] + yf[m + half] == sy
        for m in range(half)
    )

    return HalfTurnResult(
        length=len(xf),
        half_period=half,
        x_pair_sum=sx,
        y_pair_sum=sy,
        center_x=sx / 2,
        center_y=sy / 2,
        exact=exact,
    )
