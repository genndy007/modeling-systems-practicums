from dataclasses import dataclass


@dataclass(order=True)
class Channel:
    next_time: float

