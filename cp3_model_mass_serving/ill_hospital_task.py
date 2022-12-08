import random
from functools import partial

from lib_queue_sim.utils import erlang_distribution
from lib_queue_sim.structs.queues import PriorityQueue
from lib_queue_sim.log import ModelLogger
from lib_queue_sim.model.base import Model, ModelLogLevel
from lib_queue_sim.element.worker import WorkerElement
from lib_queue_sim.element.format import DefaultElementFormatter

from solutions.ill_hospital.abstract import IllPatientItem, IllPatientType
from solutions.ill_hospital.transition import (
    IllAfterLabTransition,
    IllAfterDoctorTransition,
)
from solutions.ill_hospital.create import IllCreateElement
from solutions.ill_hospital.format import IllElementFormatter
from solutions.ill_hospital.util import ElementNames

NEW_PATIENT_EXPECT = 15
NEW_PATIENT_PROBS = {
    IllPatientType.FIRST: 0.5,
    IllPatientType.SECOND: 0.1,
    IllPatientType.THIRD: 0.4,
}


def patient_type_delay_fn(item):
    ill_type_to_reg_time = {
        IllPatientType.FIRST: 15,
        IllPatientType.SECOND: 40,
        IllPatientType.THIRD: 30,
    }
    patient_time = ill_type_to_reg_time[item.type]
    return random.expovariate(lambd=1 / patient_time)


def run_hospital_simulation():
    create = IllCreateElement(
        name=ElementNames.CREATE_NAME,
        delay_fn=partial(random.expovariate, lambd=1 / NEW_PATIENT_EXPECT),
        ill_probs=NEW_PATIENT_PROBS,
    )
    at_doctor = WorkerElement(
        name=ElementNames.AT_DOCTOR_NAME,
        delay_fn=patient_type_delay_fn,
        queue=PriorityQueue(),
        channels_num=2,
    )
    doctor_to_lab = WorkerElement(
        name=ElementNames.DOCTOR_TO_LAB_NAME,
        delay_fn=partial(random.uniform, a=2, b=5),
    )
    at_lab = WorkerElement(
        name=ElementNames.AT_LAB_NAME,
        delay_fn=partial(erlang_distribution, lambd=2 / 4, k=2),
        channels_num=2,
    )
    at_registry = WorkerElement(
        name=ElementNames.AT_REGISTRY_NAME,
        delay_fn=partial(erlang_distribution, lambd=3 / 4.5, k=3),
    )
    to_palata = WorkerElement(
        name=ElementNames.TO_PALATA_NAME,
        delay_fn=partial(random.uniform, a=3, b=8),
        channels_num=3,
    )
    transition_after_doctor = IllAfterDoctorTransition(
        name=ElementNames.CHOOSE_LAB_OR_PALATA_NAME,
        to_lab=doctor_to_lab,
        to_palata=to_palata,
    )
    lab_to_doctor = WorkerElement(
        name=ElementNames.FROM_LAB_TO_DOCTOR_NAME,
        delay_fn=partial(random.uniform, a=2, b=5),
    )
    transition_after_lab = IllAfterLabTransition(
        name=ElementNames.TO_DOCTOR_OR_OUT_NAME,
        to_doctor=lab_to_doctor,
    )

    create.set_next_element(at_doctor)
    at_doctor.set_next_element(transition_after_doctor)
    doctor_to_lab.set_next_element(at_registry)
    at_registry.set_next_element(at_lab)
    at_lab.set_next_element(transition_after_lab)
    lab_to_doctor.set_next_element(at_doctor)

    logger = ModelLogger(IllElementFormatter())
    model = Model.from_create(create, logger)
    model.simulate(10000, ModelLogLevel.STATS)


if __name__ == "__main__":
    run_hospital_simulation()
