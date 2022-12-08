import random

from lib_queue_sim.element.create import CreateElement, CreateStats
from lib_queue_sim.utils import assert_probabilities_sum, MeanCalculator
from .abstract import IllPatientItem, IllPatientType


class IllCreateStats(CreateStats):
    @property
    def mean_time_by_item_type(self):
        accum = {name: MeanCalculator() for name in IllPatientType}
        for item in self.items:
            accum[item.type].add_one(item.used_time)

        name_to_mean = {name: calc.mean for name, calc in accum.items()}
        return name_to_mean

    @property
    def count_by_item_type(self):
        accum = {name: 0 for name in IllPatientType}
        for item in self.items:
            accum[item.type] += 1
        return accum


class IllCreateElement(CreateElement):
    def __init__(self, ill_probs, **kwargs):
        super().__init__(stats_cls=IllCreateStats, **kwargs)
        self.types = list(ill_probs.keys())
        self.probs = list(ill_probs.values())
        self.next_id = 0
        assert_probabilities_sum(self.probs)

    def get_next_item(self):
        self.next_id += 1
        next_type = random.choices(self.types, self.probs)[0]
        return IllPatientItem(self.next_id, self.curr_time, next_type)
