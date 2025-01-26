from genetic_algorithm.fitness.hard_constraints import (
    check_duplicate_shifts,
    check_consecutive_shifts,
    check_three_consecutive_night_shifts,
)
from genetic_algorithm.fitness.soft_constraints import (
    check_unequal_day_night_shifts,
    check_two_night_shifts,
    check_weekend_free,
    check_hierarchy_mismatch,
    check_leave_days,
)
from config.algorithm_config import initial_fitness_score


def calculate_fitness(schedule, doctors, log):
    fitness_score = initial_fitness_score

    fitness_score -= check_duplicate_shifts(schedule, log)
    fitness_score -= check_consecutive_shifts(schedule, log)
    fitness_score -= check_three_consecutive_night_shifts(schedule, log)

    fitness_score -= check_unequal_day_night_shifts(schedule, log)
    fitness_score -= check_two_night_shifts(schedule, log)
    fitness_score -= check_weekend_free(schedule, doctors, log)
    fitness_score -= check_hierarchy_mismatch(schedule, doctors, log)

    fitness_score -= check_leave_days(schedule, doctors, log)

    return fitness_score
