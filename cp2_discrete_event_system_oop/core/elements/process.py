from heapq import heapify, heappop, heappush

from core.elements.base import Element
from core.statistics.process import ProcessStatistics
from core.utils.constants import INFINITY
from core.utils.functions import set_class_instance_id


@set_class_instance_id
class Process(Element):
    def __init__(self, channels_amount, queue_max_size, delay_function):
        super().__init__(f'Process {self.instance_id()}', delay_function, ProcessStatistics(self))
        self.queue_max_size = queue_max_size
        self.channels_amount = channels_amount

        self.next_time = INFINITY
        self.queue_current_size = 0
        self.channels = []
        heapify(self.channels)

    def __str__(self):
        queue_load = self.queue_current_size / self.queue_max_size
        return 'Block ' + str(self.name) + ':\n' + \
                'Queue Load: ' + queue_load + '\n' + \
                'Next Time: ' + str(self.next_time) + '\n' + \
                'Events Amount: ' + str(self.statistics.events_amount) + '\n' + \
                'Active Channels Amount: ' + str(len(self.channels))

    def action_out(self):
        channel = heappop(self.channels)
        if self.queue_current_size != 0:
            self.queue_current_size -= 1

