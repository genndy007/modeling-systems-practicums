from abc import ABC, abstractmethod


class Collection(ABC):
    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def push(self, value):
        pass

    @abstractmethod
    def to_list(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @property
    def is_full(self):
        return False

    @property
    def is_limited(self):
        return False


class LimitedCollection(Collection):
    def __init__(self, limit_size):
        self.limit_size = limit_size

    @abstractmethod
    def get_capacity_percent(self):
        pass

    @property
    def is_full(self):
        return len(self) == self.limit_size

    @property
    def is_limited(self):
        return True
