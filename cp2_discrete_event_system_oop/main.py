from functools import partial
import random

from core.elements.create import Create
from core.elements.process import Process
from core.model import Model


def run_simulation():
    create = Create(partial(random.expovariate, lambd=1 / 0.2))
    process1 = Process(5, 10, partial(random.expovariate, lambd=1 / 1.2))
    process2 = Process(7, 8, partial(random.expovariate, lambd=1 / 2))
    process3 = Process(2, 1, partial(random.expovariate, lambd=1 / 1))

    create.add_next_element(process1, 1)
    process1.add_next_element(process2, 1)
    process2.add_next_element(process3, 1)

    model = Model(create)
    all_statistics = model.run_simulation(50, False)

    for name, statistics in all_statistics.items():
        print(name, statistics, sep='\n')


if __name__ == '__main__':
    run_simulation()