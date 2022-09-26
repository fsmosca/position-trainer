"""
"""

import math


def score_proba(score_cp):
    K = 6
    score_p = score_cp/100
    return 1 / (1 + 10 **(-score_p/K))


def expected_rating_diff(rate: float, K=600):
    """
    Calculate the expected rating difference.

    rate should not be 0 and return rd should not exceed +/- 700.

    Args:
      rate: The score rate or winning probability.

    Returns:
      The expected rating difference.
    """
    rate = min(0.99, max(0.01, rate))
    rd = -K * math.log10((1.0 - rate)/rate)
    return min(700, max(-700, rd))
