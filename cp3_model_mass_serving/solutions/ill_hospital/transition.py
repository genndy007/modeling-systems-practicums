from lib_queue_sim.element.transition import TransitionElement
from .abstract import IllPatientType


class IllAfterDoctorTransition(TransitionElement):
    def __init__(self, to_lab, to_palata, **kwargs):
        super().__init__(**kwargs)
        self.to_lab = to_lab
        self.to_palata = to_palata

    def get_adjacent_elements(self):
        return [self.to_lab, self.to_palata]

    def get_next_element(self):
        if self.item is not None and self.item.infer_type() == IllPatientType.FIRST:
            return self.to_palata
        return self.to_lab


class IllAfterLabTransition(TransitionElement):
    def __init__(self, to_doctor, **kwargs):
        super().__init__(**kwargs)
        self.to_doctor = to_doctor

    def get_adjacent_elements(self):
        return [self.to_doctor]

    def get_next_element(self):
        if self.item is not None and self.item.type == IllPatientType.SECOND:
            self.item.redirected = True
            return self.to_doctor
        return None
