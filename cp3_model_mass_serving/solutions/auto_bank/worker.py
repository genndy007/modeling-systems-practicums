from lib_queue_sim.element.worker import WorkerElement, WorkerStats


class BankWorkerStats(WorkerStats):
    def __init__(self, holder):
        super().__init__(holder)
        self.transitions_amt = 0

    def to_dict(self):
        return {
            **super().to_dict(),
            "transitions_amt": self.transitions_amt,
        }


class BankWorkerElement(WorkerElement):
    def __init__(self, transition_threshold, **kwargs):
        super().__init__(stats_cls=BankWorkerStats, **kwargs)
        self.transition_threshold = transition_threshold
        self.other = None

    def set_transition(self, other):
        self.other = other
        other.other = self

    def action_out(self):
        item = super().action_out()
        while self.is_transition_applicable():
            self.stats.transitions_amt += 1
            self.transit_item()

        return item

    def transit_item(self):
        item = self.other.queue.pop()
        self.add_to_queue(item)

    def is_transition_applicable(self):
        len_diff = len(self.other.queue) - len(self.queue)
        return len_diff >= self.transition_threshold
