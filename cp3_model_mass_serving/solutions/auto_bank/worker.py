from lib_queue_sim.element.worker import WorkerElement, WorkerStats


class BankWorkerStats(WorkerStats):
    def __init__(self, holder):
        super().__init__(holder)
        self.transitions_amt = 0

    def to_dict(self):
        return {
            **super().to_dict(),
            'transitions_amt': self.transitions_amt,
        }


