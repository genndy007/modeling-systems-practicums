from lib_queue_sim.element.transition import TransitionElement


class BankTransitionElement(TransitionElement):
    def __init__(self, name, first, second):
        super().__init__(name=name)
        self.first = first
        self.second = second

    def get_adjacent_elements(self):
        return [self.first, self.second]

    def get_next_element(self):
        if len(self.first.queue) <= len(self.second.queue):
            return self.first
        return self.second
