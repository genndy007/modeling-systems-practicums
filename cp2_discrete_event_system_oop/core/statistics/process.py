class ProcessStatistics:
    def __init__(self, element):
        self.element = element

        self.time_to_wait = 0
        self.time_to_work = 0
        self.events_amount = 0
        self.in_events_amount = 0
        self.fails_amount = 0

    def __str__(self):
        return 'STATISTICS\n' + \
                'Failure Probability: ' + str(self.get_failure_probability()) + '\n' + \
                'Mean Queue Size: ' + str(self.get_mean_queue_size()) + '\n' + \
                'Mean Active Channels: ' + str(self.get_mean_active_channels()) + '\n' + \
                'Mean Time to Wait: ' + str(self.get_mean_time_to_wait()) + '\n' + \
                'Events Amount: ' + str(self.events_amount)

    def get_failure_probability(self):
        return self.fails_amount / (self.in_events_amount or 1)

    def get_mean_queue_size(self):
        return self.events_amount / self.element.current_time

    def get_mean_active_channels(self):
        return self.time_to_work / self.element.current_time

    def get_mean_time_to_wait(self):
        return self.time_to_wait / (self.events_amount or 1)
