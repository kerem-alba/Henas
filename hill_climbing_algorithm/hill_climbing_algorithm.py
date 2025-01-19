from genetic_algorithm.initial_population import create_initial_population
from genetic_algorithm.fitness.fitness_methods import calculate_fitness
from config.algorithm_config import max_generations
from hill_climbing_algorithm.mutation_for_hill import mutate_schedule
import copy

def run_hill_climbing(doctors, doctor_mapping):
    population = create_initial_population(doctors)
    
    for generation in range(max_generations):
        with open("generation_log.txt", "a") as log_file:
            log_file.write(f"Generation {generation + 1}:\n")
            for idx, schedule in enumerate(population):
                log_file.write(f"  Individual {idx + 1}:\n")
                for day_index, day in enumerate(schedule, start=1):
                    log_file.write(f"    Day {day_index}: {day}\n")

       
            for idx in range(len(population)):
                # Orijinal bireyi seç
                original = population[idx]

                # Orijinal bireyin fitness'ını hesapla
                original_fitness = calculate_fitness(original, doctors, doctor_mapping)

                # Orijinal bireyin kopyasına mutasyon uygula
                mutated = mutate_schedule(copy.deepcopy(original))
                mutated_fitness = calculate_fitness(mutated, doctors, doctor_mapping)

                # Eğer mutasyonlu birey daha iyiyse, popülasyondaki yerini al
                if mutated_fitness > original_fitness:
                    population[idx] = mutated
                    log_file.write(f"  Individual {idx + 1}: Fitness Improved from {original_fitness} to {mutated_fitness}\n")
                else:
                    log_file.write(f"  Individual {idx + 1}: Fitness Remained at {original_fitness}\n")

    # En iyi bireyi bul
    best_individual = max(population, key=lambda x: calculate_fitness(x, doctors, doctor_mapping))
    best_fitness = calculate_fitness(best_individual, doctors, doctor_mapping)

    # En iyi bireyi ve fitness'ını yazdır
    print("\nBest Individual:")
    for day_index, day in enumerate(best_individual, start=1):
        print(f"Day {day_index}: {day}")
    print("Fitness Score:", best_fitness)

    return best_individual