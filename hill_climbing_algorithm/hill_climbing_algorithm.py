from genetic_algorithm.initial_population import create_initial_population
from genetic_algorithm.fitness.fitness_methods import calculate_fitness
from config.algorithm_config import (
    max_generations,
    doctor_swap_rate,
    doctor_slide_rate,
    shift_swap_rate,
    day_swap_rate,
)
from genetic_algorithm.mutation.mutation_methods import mutate_schedule
import copy


def run_hill_climbing(doctors):

    population = create_initial_population(doctors)

    for generation in range(max_generations):

        doc_rate, slide_rate, shift_rate, day_rate = get_swap_rates(generation)

        for idx in range(len(population)):
            original = population[idx]
            original_fitness = calculate_fitness(original, doctors, log=False)
            mutated = mutate_schedule(
                copy.deepcopy(original), doc_rate, slide_rate, shift_rate, day_rate
            )
            mutated_fitness = calculate_fitness(mutated, doctors, log=False)

            if mutated_fitness > original_fitness:
                population[idx] = mutated
                with open("generation_log.txt", "a") as log_file:
                    log_file.write(f"Generation {generation + 1}:\n")
                    log_file.write(f"  Individual {idx + 1}:\n")
                    for day_index, day in enumerate(mutated, start=1):
                        log_file.write(f"    Day {day_index}: {day}\n")
                    log_file.write(
                        f"  Fitness Improved from {original_fitness} to {mutated_fitness}\n"
                    )
            else:
                with open("generation_log.txt", "a") as log_file:
                    log_file.write(f"Generation {generation + 1}:\n")
                    log_file.write(f"  Individual {idx + 1}:\n")
                    log_file.write(f"  Fitness Remained at {original_fitness}\n")

    return process_population(population, doctors)


def process_population(population, doctors):
    processed_population = []

    for idx in range(len(population)):
        # Schedule'ı işle
        population[idx] = sort_doctors_in_shifts(population[idx])

        # Fitness puanını hesapla
        fitness_score = calculate_fitness(population[idx], doctors, log=True)

        # Schedule ve fitness puanını birlikte sakla
        processed_population.append((population[idx], fitness_score))

    # Log dosyasına yaz
    with open("generation_log.txt", "a") as log_file:
        for idx, (schedule, fitness_score) in enumerate(processed_population):
            log_file.write(f"\nIndividual {idx + 1} Final Schedule:\n")
            for day_index, day in enumerate(schedule, start=1):
                log_file.write(f"  Day {day_index}: {day}\n")
            log_file.write(f"  Fitness Score: {fitness_score}\n")

    return processed_population


def get_swap_rates(generation):
    if generation < 1000:
        return doctor_swap_rate, doctor_slide_rate, shift_swap_rate, day_swap_rate
    elif generation < 2000:
        return 0.4, 0.4, 0.1, 0.1
    else:
        return 0.8, 0.2, 0, 0


def sort_doctors_in_shifts(schedule):
    for day in schedule:
        for shift in day:
            shift.sort()
    return schedule
