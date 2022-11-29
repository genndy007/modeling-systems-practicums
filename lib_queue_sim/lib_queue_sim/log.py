import logging
import sys
from abc import ABC
from operator import attrgetter

from lib_queue_sim.element.format import DefaultElementFormatter


class Logger(ABC):
    logging.basicConfig(format="%(message)s")

    def __init__(self, name, handler=logging.StreamHandler(sys.stdout)):
        self.logger = logging.getLogger(name)
        self.logger.propagate = False
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log(self, message):
        self.logger.info(message)


class ModelLogger(Logger):
    def __init__(self, formatter=DefaultElementFormatter()):
        super().__init__(__name__)
        self.formatter = formatter

    def __sorted_elements(self, elements):
        return sorted(elements, key=lambda el: el.name)

    def log_current_state(self, curr_time, elements):
        self.log(self.formatter.format_curr_time(curr_time))
        for element in self.__sorted_elements(elements):
            self.log(self.formatter.format_element_state(element))
        self.log(self.formatter.format_divider(line_width=75))

    def log_statistics(self, elements):
        self.log("\n")
        self.log("STATISTICS:")
        for element in self.__sorted_elements(elements):
            self.log(self.formatter.format_divider())
            self.log(f"{element.name}:")
            self.log(self.formatter.format_stats(element))
        self.log(self.formatter.format_divider())

    def log_totals(self, totals):
        self.log("\n")
        self.log("TOTALS:")
        self.log(self.formatter.format_dict(totals))
