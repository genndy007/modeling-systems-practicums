from lib_queue_sim.element.create import CreateElement
from lib_queue_sim.element.worker import WorkerElement
from lib_queue_sim.log import ModelLogger
from lib_queue_sim.model.stats import ModelStats, ModelLogLevel
from lib_queue_sim.utils import TIME_EPSILON


class Model:
    def __init__(self, elements, logger=ModelLogger()):
        self.elements = elements
        self.logger = logger
        self.curr_time = 0
        self.stats = ModelStats(self)

    @classmethod
    def from_create(cls, create, logger):
        elements = Model._retrieve_elements(create)
        return cls(elements, logger)

    def simulate(self, stop_time, level=ModelLogLevel):
        while self.curr_time < stop_time:
            self.curr_time = self._get_curr_time()
            self._set_curr_time(self.curr_time)
            self._process_elements(self.curr_time)

            if level == ModelLogLevel.CURRENT_STATE:
                self.logger.log_current_state(self.curr_time, self.elements)

        if level == ModelLogLevel.STATS:
            self.logger.log_statistics(self.elements)

        return self._finalize_stats()

    def reset(self):
        self.stats.reset()
        for element in self.elements:
            element.reset()
        self.curr_time = 0

    def _process_elements(self, curr_time):
        for element in self.elements:
            if abs(element.next_time - curr_time) > TIME_EPSILON:
                continue

            element.action_out()
            if isinstance(element, (CreateElement, WorkerElement)):
                self.stats.events_amount += 1

    def _get_curr_time(self):
        min_el = min(self.elements, key=lambda el: el.next_time)
        return min_el.next_time

    def _set_curr_time(self, next_time):
        for element in self.elements:
            element.set_curr_time(next_time)

    def _finalize_stats(self):
        element_stats = {element.name: element.stats for element in self.elements}
        return self.stats, element_stats

    @staticmethod
    def _retrieve_elements(root_element):
        elements = set()

        def go_inside_element(root_element):
            elements.add(root_element)
            for element in root_element.get_adjacent_elements():
                if element is not None and element not in elements:
                    go_inside_element(element)

        go_inside_element(root_element)
        return list(elements)
