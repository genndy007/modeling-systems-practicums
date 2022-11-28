import inspect
import uuid
from abc import ABC, abstractmethod

from lib_queue_sim.utils import StatsResetable, zero_fn


class Item:
    def __init__(self, item_id, created_at):
        self.item_id = item_id
        self.created_at = created_at
        self.updated_at = None

    @property
    def used_time(self):
        return self.updated_at - self.created_at


class ElementStats(StatsResetable):
    def __init__(self, holder):
        super().__init__(holder)
        self.out_amount = 0
        self.in_amount = 0

    def to_dict(self):
        return {
            "in_amount": self.in_amount,
            "out_amount": self.out_amount,
        }


class Element(ABC):
    def __init__(self, delay_fn=zero_fn, name=None, stats_cls=ElementStats):
        self.name = name if name else self._random_name()
        self.delay_fn = delay_fn
        self._delay_args = inspect.signature(self.delay_fn).parameters
        self.stats = stats_cls(self)
        self.curr_time = 0
        self.next_time = 0
        self.next_element = None

    @abstractmethod
    def action_in(self, item):
        self.handler_in()

    @abstractmethod
    def action_out(self):
        pass

    def handler_in(self):
        self.stats.in_amount += 1

    def handler_out(self):
        self.stats.out_amount += 1

    def get_adjacent_elements(self):
        return [self.next_element]

    def pass_item(self, item):
        item.updated_at = self.curr_time
        next_element = self.get_next_element()
        if next_element is not None:
            next_element.action_in(item)
        self.handler_out()

    def get_next_element(self):
        return self.next_element

    def set_next_element(self, next_element):
        self.next_element = next_element

    def set_curr_time(self, next_time):
        self.curr_time = next_time

    def get_next_time(self, **kwargs):
        fn_kwargs = {
            name: value for name, value in kwargs.items() if name in self._delay_args
        }
        return self.curr_time + self.delay_fn(**fn_kwargs)

    def reset(self):
        self.stats.reset()
        self.curr_time = 0
        self.next_time = 0

    def _random_name(self):
        hash_code = uuid.uuid4().hex[0:6]
        return f"{self.__class__.__name__}-{hash_code}"
