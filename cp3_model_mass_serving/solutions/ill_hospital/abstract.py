from enum import Enum
from functools import total_ordering

from lib_queue_sim.element.abstract import Item


class IllPatientType(Enum):
    FIRST = 1  # Overcame previous looking and go to healing
    SECOND = 2  # Want to hospital, but not fully overcame previous looking
    THIRD = 3  # Only going to previous looking


@total_ordering
class IllPatientItem(Item):
    def __init__(self, item_id, created_at, id, type, redirected=False):
        super().__init__(item_id, created_at)
        self.id = id
        self.type = type
        self.redirected = redirected

    def infer_type(self):
        if self.redirected:
            return IllPatientType.FIRST
        return self.type

    def __lt__(self, other):
        if self.infer_type() == other.infer_type():
            return self.created_at < other.created_at
        return self.infer_type() == IllPatientType.FIRST
