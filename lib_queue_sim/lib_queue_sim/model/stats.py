from enum import Enum, auto
from lib_queue_sim.utils import StatsResetable, TIME_EPSILON


class ModelLogLevel(Enum):
    SILENT = auto()
    CURRENT_STATE = auto()
    STATS = auto()


class ModelStats(StatsResetable):
    def __init__(self, holder):
        super().__init__(holder)
        self.events_amount = 0

    @property
    def intensity(self):
        return self.events_amount / max(self.holder.curr_time, TIME_EPSILON)
