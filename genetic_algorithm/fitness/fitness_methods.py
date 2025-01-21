from genetic_algorithm.fitness.hard_constraints import (
    check_duplicate_shifts,
    check_consecutive_shifts,
    check_three_consecutive_night_shifts,
    check_coverage_in_shift,
)
from genetic_algorithm.fitness.soft_constraints import check_unequal_day_night_shifts, check_two_night_shifts, check_weekend_free, check_hierarchy_mismatch
from config.algorithm_config import initial_fitness_score

def calculate_fitness(schedule, doctors, doctor_mapping, seniority_levels, log):
    fitness_score = initial_fitness_score

    fitness_score -= check_duplicate_shifts(schedule, log)
    fitness_score -= check_consecutive_shifts(schedule, log)
    fitness_score -= check_three_consecutive_night_shifts(schedule, log)
    #fitness_score -= check_coverage_in_shift(schedule, doctor_mapping, seniority_levels, log)

    fitness_score -= check_unequal_day_night_shifts(schedule,log)
    fitness_score -= check_two_night_shifts(schedule,log)
    fitness_score -= check_weekend_free(schedule, doctors, log)
    fitness_score -= check_hierarchy_mismatch(schedule,doctor_mapping,log)

    return fitness_score

