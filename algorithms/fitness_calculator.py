from algorithms.hard_constraints import (
    check_duplicate_shifts,
    check_consecutive_shifts,
    check_three_consecutive_night_shifts,
    check_coverage_in_shift
)
from config.algorithm_config import initial_fitness_score

def calculate_fitness(schedule, doctors):
    fitness_score = initial_fitness_score

    fitness_score -= check_duplicate_shifts(schedule)
    fitness_score -= check_consecutive_shifts(schedule)
    fitness_score -= check_three_consecutive_night_shifts(schedule)
    fitness_score -= check_coverage_in_shift(schedule, doctors)

    return fitness_score
