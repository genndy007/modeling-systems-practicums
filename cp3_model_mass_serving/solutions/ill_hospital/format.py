from lib_queue_sim.element.format import DefaultElementFormatter
from lib_queue_sim.element.abstract import Element
from .create import IllCreateElement


class IllElementFormatter(DefaultElementFormatter):
    def format_stats(self, element):
        if isinstance(element, IllCreateElement):
            return
        return super().format_stats(element)

    def format_ill_create_stats(self, element):
        tab_tab = "\t\t"
        stats_str = (
            f"{self.format_dict(element.stats.to_dict())}\n\t"
            f"Mean time by Item type:\n{self.format_dict(element.stats.mean_time_by_item_type, tab_tab)}\n\t"
            f"Count by Item type:\n{self.format_dict(element.stats.count_by_item_type, tab_tab)}"
        )
        return stats_str
