from core.element import Element
from core.statistics.process import ProcessStatistics
from core.utils import set_class_instance_id


class Channel:
    def __init__(self, next_time):
        self.next_time = next_time


@set_class_instance_id
class Process(Element):
    def __init__(self, channels_amount, queue_size, delay_function):
        super().__init__(f'Process {self.instance_id()}', delay_function, ProcessStatistics(self))
