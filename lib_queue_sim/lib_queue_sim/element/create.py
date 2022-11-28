from abc import abstractmethod

from lib_queue_sim.element.abstract import ElementStats, Element, Item
from lib_queue_sim.utils import MeanCalculator


class CreateStats(ElementStats):
    def __init__(self, holder):
        super().__init__(holder)
        self.items = []

    @property
    def mean_used_time(self):
        calculator = MeanCalculator()
        for item in self.items:
            calculator.add_one(item.used_time)
        return calculator.mean

    def add_item(self, item):
        self.items.append(item)

    def to_dict(self):
        return {
            **super().to_dict(),
            "mean_used_time": self.mean_used_time,
        }


class Create(Element):
    def __init__(self, stats_cls=CreateStats, **kwargs):
        super().__init__(stats_cls=stats_cls, **kwargs)

    def action_in(self, item):
        raise RuntimeError('Action IN impossible, it is CREATE')

    def action_out(self):
        self.next_time = self.get_next_time()
        item = self.get_next_item()
        self.stats.add_item(item)
        super().pass_item(item)

    @abstractmethod
    def get_next_item(self):
        pass


class DefaultCreate(Create):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_id = 0

    def get_next_item(self):
        self.next_id += 1
        return Item(self.next_id, self.curr_time)
