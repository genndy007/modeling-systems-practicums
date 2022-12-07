from solutions.auto_bank.worker import BankWorkerElement


def calculate_mean_clients_amt(workers):
    total = 0
    for worker in workers:
        mean_clients = worker.stats.mean_queue_size + worker.stats.mean_active_channels
        total += mean_clients
    return total


def calculate_total_failure_probability(workers):
    total_in, total_fails_amt = 0, 0
    for worker in workers:
        total_in += worker.stats.in_amount
        total_fails_amt += worker.stats.fails_amount

    total_fail_prob = total_fails_amt / max(total_in, 1)
    return total_fail_prob


def calculate_total_transitions(workers):
    total = 0
    for worker in workers:
        total += worker.stats.transitions_amt
    return total
