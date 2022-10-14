from core.utils.constants import EPSILON


class Model:
    def __init__(self, root):
        self.elements = self.__create_elements_list(root)
        self.elements.sort(key=lambda el: el.name)

    def run_simulation(self, given_time, print_statistics=False):
        current_time = 0
        while current_time < given_time:
            current_time = self.__get_current_time()
            self.__set_current_time(current_time)
            self.__action_elements(current_time)
            if print_statistics:
                self.__pprint_statistics(current_time)

        return self.__get_all_elements_statistics()

    def __create_elements_list(self, root):
        elements = set()

        def recursive_add(root):
            elements.add(root)
            for element in root.next_elements:
                if element not in elements:
                    recursive_add(element)

        recursive_add(root)
        return list(elements)

    def __action_elements(self, current_time):
        for element in self.elements:
            time_difference = abs(element.next_time - current_time)
            if time_difference < EPSILON:
                element.action_out()

    def __get_current_time(self):
        minimal_element = min(self.elements, key=lambda el: el.next_time)
        return minimal_element.next_time

    def __set_current_time(self, next_time):
        for element in self.elements:
            element.set_current_time(next_time)

    def __get_all_elements_statistics(self):
        return {
            element.name: element.statistics
            for element in self.elements
        }

    def __pprint_statistics(self, current_time):
        text = '\n'.join(str(element) for element in self.elements)
        print(f'Time({current_time:.3f}):\n{text}\n')