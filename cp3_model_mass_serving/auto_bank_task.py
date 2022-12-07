import random
from functools import partial

from lib_queue_sim.structs.queues import LimitedQueue
from lib_queue_sim.log import ModelLogger
from lib_queue_sim.model.base import Model, ModelLogLevel
from lib_queue_sim.element.abstract import Item
from lib_queue_sim.element.create import DefaultCreateElement
from lib_queue_sim.element.worker import Channel
from lib_queue_sim.element.format import DefaultElementFormatter

from solutions.auto_bank.worker import BankWorkerElement
from solutions.auto_bank.transition import BankTransitionElement
from solutions.auto_bank.calculate import (
    calculate_total_transitions,
    calculate_total_failure_probability,
    calculate_mean_clients_amt,
)

AUTO_COMING_EXPECT = 0.5
CASHIER_SERVING_EXPECT = 0.3
LINE_QUEUE_SIZE = 3
QUEUE_SIZE_DIFF_TO_TRANSIT = 2

FIRST_CLIENT_TIME = 0.1

CREATE_NAME = "1. Automobilists Coming"
TRANSITION_NAME = "2. Choosing between Cassa1 and Cassa2"
CASSA_1_NAME = "3. Cassa Nomer 1"
CASSA_2_NAME = "4. Cassa Nomer 2"


def normal_var(mu, sigma):
    return random.normalvariate(mu, sigma)


def run_bank_simulation():
    create = DefaultCreateElement(
        name=CREATE_NAME,
        delay_fn=partial(random.expovariate, lambd=1 / AUTO_COMING_EXPECT),
    )
    first_cassa = BankWorkerElement(
        name=CASSA_1_NAME,
        delay_fn=partial(random.expovariate, lambd=1 / CASHIER_SERVING_EXPECT),
        queue=LimitedQueue(limit_size=LINE_QUEUE_SIZE),
        channels_num=1,
        transition_threshold=QUEUE_SIZE_DIFF_TO_TRANSIT,
    )
    second_cassa = BankWorkerElement(
        name=CASSA_2_NAME,
        delay_fn=partial(random.expovariate, lambd=1 / CASHIER_SERVING_EXPECT),
        queue=LimitedQueue(limit_size=LINE_QUEUE_SIZE),
        channels_num=1,
        transition_threshold=QUEUE_SIZE_DIFF_TO_TRANSIT,
    )

    first_cassa.set_transition(second_cassa)
    transition = BankTransitionElement(TRANSITION_NAME, first_cassa, second_cassa)
    create.set_next_element(transition)

    for cassa in first_cassa, second_cassa:
        cassa.add_channel(
            Channel(create.get_next_item(), normal_var(1, CASHIER_SERVING_EXPECT))
        )
    for _ in range(2):
        first_cassa.queue.push(create.get_next_item())
        second_cassa.queue.push(create.get_next_item())

    create.next_time = FIRST_CLIENT_TIME

    logger = ModelLogger()  # DefaultElementFormatter()
    model = Model.from_create(create, logger)
    model.simulate(10000, ModelLogLevel.STATS)

    workers = [first_cassa, second_cassa]
    totals = {
        "fail_probability": calculate_total_failure_probability(workers),
        "transitions_num": calculate_total_transitions(workers),
        "mean_clients_amt": calculate_mean_clients_amt(workers),
    }
    logger.log_totals(totals)


if __name__ == "__main__":
    run_bank_simulation()
