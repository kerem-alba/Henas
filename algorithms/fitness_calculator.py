from algorithms.hard_constraints import (
    check_duplicate_shifts,
    check_consecutive_shifts,
    check_three_consecutive_night_shifts,
    check_coverage_in_shift,
)
from algorithms.soft_constraints import check_unequal_day_night_shifts, check_two_night_shifts, check_weekend_free, check_hierarchy_mismatch

from config.algorithm_config import initial_fitness_score

def calculate_fitness(schedule, doctors, doctor_mapping):
    fitness_score = initial_fitness_score

    fitness_score -= check_duplicate_shifts(schedule)
    fitness_score -= check_consecutive_shifts(schedule)
    fitness_score -= check_three_consecutive_night_shifts(schedule)
    print("fs1",fitness_score)
    fitness_score -= check_coverage_in_shift(schedule, doctors)
    print("fs2",fitness_score)


    fitness_score -= check_unequal_day_night_shifts(schedule)
    fitness_score -= check_two_night_shifts(schedule)
    fitness_score -= check_weekend_free(schedule, doctors)
    fitness_score -= check_hierarchy_mismatch(schedule,doctors, doctor_mapping)

    return fitness_score
