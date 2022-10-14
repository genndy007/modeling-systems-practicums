import random

from core.statistics import Statistics


class Element:
    def __init__(self, name, delay_function, statistics=Statistics()):
        self.name = name
        self.delay_function = delay_function
        self.statistics = statistics

        self.current_time = 0
        self.next_time = 0
        self.next_elements = []
        self.next_probabilities = []

    def action_out(self):
        self.statistics.events_amount += 1
        next_element = self.__get_next_element()
        if next_element:
            next_element.action_in()

    def action_in(self):
        pass

    def add_next_element(self, element, probability):
        self.next_elements.append(element)
        self.next_probabilities.append(probability)

    def set_current_time(self, next_time):
        self.current_time = next_time

    def __check_probabilities(self):
        probabilities_sum = sum(self.next_probabilities)
        if probabilities_sum != 1:
            print('Sum of probabilities expected to be 1, but we have it', probabilities_sum)
            return False
        return True

    def __get_next_element(self):
        if self.next_elements and self.__check_probabilities():
            next_element = random.choices(self.next_elements, self.next_probabilities)[0]
            return next_element
        return None

    def __get_next_time(self):
        next_time = self.current_time + self.delay_function()
        return next_time



