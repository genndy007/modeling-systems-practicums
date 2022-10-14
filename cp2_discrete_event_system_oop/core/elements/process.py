from heapq import heapify, heappop, heappush

from core.elements.base import Element
from core.statistics.process import ProcessStatistics
from core.utils.classes import Channel
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
        return 'Block '  + ':\n' + \
               'Queue Load: ' + queue_load + '\n' + \
               'Next Time: ' + str(self.next_time) + '\n' + \
               'Events Amount: ' + str(self.statistics.events_amount) + '\n' + \
               'Active Channels Amount: ' + str(len(self.channels))

    def action_out(self):
        channel = heappop(self.channels)
        if self.queue_current_size != 0:
            self.queue_current_size -= 1
            channel.next_time = self.get_next_time()
            heappush(self.channels, channel)

        if self.channels:
            self.next_time = self.channels[0].next_time
        else:
            self.next_time = INFINITY

        super().action_out()

    def action_in(self):
        self.statistics.in_events_amount += 1
        if len(self.channels) == self.channels_amount:
            self.__enqueue()
        else:
            self.__add_channel()

    def set_current_time(self, next_time):
        time_difference = next_time - self.current_time
        self.statistics.time_to_wait += time_difference * self.queue_current_size
        self.statistics.time_to_work += time_difference * len(self.channels)
        super().set_current_time(next_time)

    def __enqueue(self):
        if self.queue_current_size < self.queue_max_size:
            self.queue_current_size += 1
        else:
            self.statistics.fails_amount += 1

    def __add_channel(self):
        channel = Channel(self.get_next_time())
        heappush(self.channels, channel)
        self.next_time = self.channels[0].next_time
