from core.element import Element


class Create(Element):
    def __init__(self, delay_function):
        super().__init__('Create', delay_function)

    def __str__(self):
        return 'Block ' + self.name + ':\n' + \
               'Next Time == ' + str(self.next_time) + '\n' + \
               'Events Amount == ' + str(self.statistics.events_amount)

    def action_out(self):
        self.next_time = self.get_next_time()
        super().action_out()