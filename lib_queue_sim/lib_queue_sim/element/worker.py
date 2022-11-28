from lib_queue_sim.element.abstract import ElementStats, Element
from lib_queue_sim.structs.queues import Queue, PriorityQueue, LimitedPriorityQueue
from lib_queue_sim.utils import TIME_EPSILON, TIME_INFINITE


class Channel:
    def __init__(self, item, next_time):
        self.item = item
        self.next_time = next_time


class WorkerStats(ElementStats):
    def __init__(self, holder):
        super().__init__(holder)
        self.wait_time = 0
        self.work_time = 0
        self.fails_amount = 0

        self.in_time = 0
        self.out_time = 0
        self.in_interval = 0
        self.out_interval = 0

    @property
    def mean_queue_size(self):
        return self.wait_time / max(self.holder.curr_time, TIME_EPSILON)

    @property
    def fail_probability(self):
        return self.fails_amount / max(self.in_amount, 1)

    @property
    def mean_active_channels(self):
        return self.work_time / max(self.holder.curr_time, TIME_EPSILON)

    @property
    def mean_wait_time(self):
        return self.wait_time / max(self.out_amount, 1)

    @property
    def mean_in_interval(self):
        return self.in_interval / max(self.in_amount, 1)

    @property
    def mean_out_interval(self):
        return self.out_interval / max(self.out_amount, 1)

    def to_dict(self):
        return {
            **super().to_dict(),
            "mean_queue_size": self.mean_queue_size,
            "fail_probability": self.fail_probability,
            "mean_active_channels": self.mean_active_channels,
            "mean_wait_time": self.mean_wait_time,
            "mean_in_interval": self.mean_in_interval,
            "mean_out_interval": self.mean_out_interval,
        }


class WorkerElement(Element):
    def __init__(
        self, queue=Queue(), channels_num=None, stats_cls=WorkerStats, **kwargs
    ):
        super().__init__(stats_cls=stats_cls, **kwargs)
        self.channels = (
            PriorityQueue()
            if channels_num is None
            else LimitedPriorityQueue(channels_num)
        )
        self.queue = queue
        self.next_time = TIME_INFINITE

    def action_in(self, item):
        super().action_in(item)
        if self.channels.is_full:
            self.add_to_queue(item)
        else:
            channel = Channel(item, self.get_next_time(item=item))
            self.add_channel(channel)

    def action_out(self):
        item = self.channels.pop().item

        if len(self.queue) != 0:
            next_item = self.queue.pop()
            channel = Channel(next_item, self.get_next_time(item=item))
            self.add_channel(channel)
        else:
            self.next_time = self.get_next_channels_time()

        self.pass_item(item)
        return item

    def handler_in(self):
        super().handler_in()
        if self.stats.in_amount > 1:
            self.stats.in_interval += self.curr_time - self.stats.in_time
        self.stats.in_time = self.curr_time

    def handler_out(self):
        super().handler_out()
        if self.stats.out_amount > 1:
            self.stats.out_interval += self.curr_time - self.stats.out_time
        self.stats.out_time = self.curr_time

    def set_curr_time(self, next_time):
        diff_time = next_time - self.curr_time
        self.stats.wait_time += diff_time * len(self.queue)
        self.stats.work_time += diff_time * len(self.channels)
        super().set_curr_time(next_time)

    def add_channel(self, channel):
        self.channels.push(channel)
        self.next_time = self.get_next_channels_time()

    def reset(self):
        super().reset()
        self.channels.clear()
        self.queue.clear()
        self.next_time = TIME_INFINITE

    def get_next_channels_time(self):
        if len(self.channels) == 0:
            return TIME_INFINITE
        return self.channels.to_list()[0].next_time

    def add_to_queue(self, item):
        if not self.queue.is_full:
            self.queue.push(item)
        else:
            self.stats.fails_amount += 1
