from dataclasses import dataclass, fields, _MISSING_TYPE
import random
import sys
from math import log

TIME_INFINITE = float("inf")
TIME_EPSILON = sys.float_info.epsilon


def zero_fn(**kwargs):
    return 0


def erlang_distribution(lambd, k):
    product = 1
    for _ in range(k):
        product *= random.random()

    result = -1 / lambd * log(product)
    return result


def float_formatting(value):
    return f"{value:.3f}"


def assert_probabilities_sum(probs):
    probs_sum = sum(probs)
    if probs_sum != 1:
        raise RuntimeError(f"Sum of Probabilities expected to be 1, got {probs_sum}")


class MeanCalculator:
    def __init__(self):
        self.sum = 0
        self.count = 0

    def add_one(self, value):
        self.count += 1
        self.sum += value

    @property
    def mean(self):
        return self.sum / max(self.count, 1)


@dataclass()
class StatsResetable:
    def __init__(self, holder):
        self.holder = holder

    def reset(self):
        for field in fields(self):
            if not isinstance(field.default, _MISSING_TYPE):
                setattr(self, field.name, field.default)
            elif not isinstance(field.default_factory, _MISSING_TYPE):
                setattr(self, field.name, field.default_factory())
