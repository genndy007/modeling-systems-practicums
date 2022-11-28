from heapq import heapify, heappop, heappush

from lib_queue_sim.structs.collections import Collection, LimitedCollection


class Queue(Collection):
    def __init__(self):
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def pop(self):
        return self.queue.pop()

    def push(self, value):
        self.queue.append(value)

    def to_list(self):
        return self.queue

    def clear(self):
        self.queue = []


class PriorityQueue(Collection):
    def __init__(self):
        super().__init__()
        self.queue = []
        heapify(self.queue)

    def __len__(self):
        return len(self.queue)

    def pop(self):
        return heappop(self.queue)

    def push(self, value):
        return heappush(self.queue, value)

    def to_list(self):
        return self.queue

    def clear(self):
        self.queue = []


class LimitedQueue(LimitedCollection, Queue):
    def __init__(self, limit_size):
        super().__init__(limit_size)
        self.queue = []

    def push(self, value):
        if not self.is_full:
            self.queue.append(value)

    def get_capacity_percent(self):
        return len(self) / self.limit_size


class LimitedPriorityQueue(LimitedCollection, PriorityQueue):
    def __init__(self, limit_size):
        super().__init__(limit_size)
        self.queue = []
        heapify(self.queue)

    def push(self, value):
        if not self.is_full:
            heappush(self.queue, value)

    def get_capacity_percent(self):
        return len(self) / self.limit_size
