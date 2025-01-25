from genetic_algorithm.initial_population import create_initial_population
from genetic_algorithm.fitness.fitness_methods import calculate_fitness
from config.algorithm_config import max_generations, doctor_swap_rate, doctor_slide_rate, shift_swap_rate, day_swap_rate
from genetic_algorithm.mutation.mutation_methods import mutate_schedule
import json
import copy


def run_hill_climbing(doctors, doctor_mapping):

    population = create_initial_population(doctors)

    with open("data/leaves.json", "r") as file:
        leaves_data = json.load(file)

    leaves = leaves_data["leaves"]
    leave_dict = {leave["code"]: {"optional_leaves": leave["optional_leaves"], "mandatory_leaves": leave["mandatory_leaves"]} for leave in leaves}

    found_1000_fitness = False
    for generation in range(max_generations):

        doc_rate, slide_rate, shift_rate, day_rate = get_swap_rates(generation)

        for idx in range(len(population)):
            original = population[idx]
            original_fitness = calculate_fitness(original, doctors, doctor_mapping, leave_dict, log=False)
            mutated = mutate_schedule(copy.deepcopy(original), doc_rate, slide_rate, shift_rate, day_rate)
            mutated_fitness = calculate_fitness(mutated, doctors, doctor_mapping, leave_dict, log=False)

            if mutated_fitness > original_fitness:
                population[idx] = mutated
                with open("generation_log.txt", "a") as log_file:
                    log_file.write(f"Generation {generation + 1}:\n")
                    log_file.write(f"  Individual {idx + 1}:\n")
                    for day_index, day in enumerate(mutated, start=1):
                        log_file.write(f"    Day {day_index}: {day}\n")
                    log_file.write(f"  Fitness Improved from {original_fitness} to {mutated_fitness}\n")
            else:
                with open("generation_log.txt", "a") as log_file:
                    log_file.write(f"Generation {generation + 1}:\n")
                    log_file.write(f"  Individual {idx + 1}:\n")
                    log_file.write(f"  Fitness Remained at {original_fitness}\n")

            if mutated_fitness == 1000:
                found_1000_fitness = True
                break

        if found_1000_fitness:
            break
        
    for idx in range(len(population)):
        population[idx] = sort_doctors_in_shifts(population[idx])

        with open("generation_log.txt", "a") as log_file:
            
            for idx, schedule in enumerate(population):
                log_file.write(f"\nIndividual {idx + 1} Final Schedule:\n")
                for day_index, day in enumerate(schedule, start=1):
                    log_file.write(f"  Day {day_index}: {day}\n")
                
                log_file.write(f"\nIndividual {idx + 1} Penalties:\n")
                print("Final Score: ",calculate_fitness(schedule, doctors, doctor_mapping, leave_dict, log=True))

    return population

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