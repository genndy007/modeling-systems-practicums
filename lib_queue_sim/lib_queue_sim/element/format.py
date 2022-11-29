from abc import ABC, abstractmethod

from lib_queue_sim.element.create import CreateElement
from lib_queue_sim.element.worker import WorkerElement
from lib_queue_sim.utils import float_formatting


class ElementFormatter(ABC):
    def format_curr_time(self, curr_time):
        return f"Time({float_formatting(curr_time)}):"

    def format_divider(self, line_width=50, divider="-"):
        return divider * line_width

    def format_tab(self):
        return "\t"

    @abstractmethod
    def format_element_state(self, element):
        pass

    @abstractmethod
    def format_stats(self, element):
        pass

    @abstractmethod
    def format_dict(self, dictionary):
        pass


class DefaultElementFormatter(ElementFormatter):
    def format_collection_capacity(self, queue):
        if not queue.is_limited:
            return f"{len(queue)}"
        else:
            return f"{len(queue)}/{queue.limit_size}"

    def format_abstract_state(self, element):
        return f"Events_Amount={element.stats.out_amount}"

    def format_create_state(self, element):
        return (
            f"{self.format_abstract_state(element)}, "
            f"next_time={float_formatting(element.next_time)}"
        )

    def format_worker_state(self, element):
        return (
            f"{self.format_abstract_state(element)},"
            f"next_time={float_formatting(element.next_time)}"
            f"queue_load={self.format_collection_capacity(element.queue)}"
            f"channels_load={self.format_collection_capacity(element.channels)}"
        )

    def get_state(self, element):
        if isinstance(element, WorkerElement):
            return self.format_worker_state(element)
        if isinstance(element, CreateElement):
            return self.format_create_state(element)
        return self.format_abstract_state(element)

    def format_element_state(self, element):
        state_str = self.get_state(element)
        return f"[{element.name}]: {state_str}"

    def format_dict(self, dictionary, tab="\t"):
        formatted_items = []
        for stat_key, stat_value in dictionary.items():
            formatted_item = f"{tab}{stat_key}: {float_formatting(stat_value)}"
            formatted_items.append(formatted_item)

        return "\n".join(formatted_items)

    def format_stats(self, element):
        stats_dict = element.stats.to_dict()
        return self.format_dict(stats_dict)
