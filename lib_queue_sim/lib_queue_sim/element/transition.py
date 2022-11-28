from abc import abstractmethod
from random import choices

from lib_queue_sim.element.abstract import Element
from lib_queue_sim.utils import TIME_INFINITE, assert_probabilities_sum


class TransitionElement(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_time = TIME_INFINITE
        self.item = None

    def action_in(self, item):
        super().action_in(item)
        self.item = item
        self.next_time = self.get_next_time()

    def action_out(self):
        self.next_time = TIME_INFINITE
        self.pass_item(self.item)

    @abstractmethod
    def get_next_element(self):
        pass

    @abstractmethod
    def get_adjacent_elements(self):
        pass


class ProbTransitionElement(TransitionElement):
    def __init__(self, next_elements, **kwargs):
        super().__init__(**kwargs)
        self.next_elements = list(next_elements.keys())
        self.next_probs = list(next_elements.values())

    def get_adjacent_elements(self):
        return self.next_elements

    def add_next_element(self, element, prob):
        self.next_elements.append(element)
        self.next_probs.append(prob)

    def get_next_element(self):
        if self.next_elements:
            assert_probabilities_sum(self.next_probs)
            return choices(self.next_elements, self.next_probs)[0]
