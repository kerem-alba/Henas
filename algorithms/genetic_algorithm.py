from algorithms.initial_population import create_initial_population
from algorithms.fitness.fitness_methods import calculate_fitness
from algorithms.selection.selection_methods import handle_elites, random_preselect_tournament_pool, create_parent_pool_from_pairs

def run_genetic_algorithm(doctors, doctor_mapping, days, shifts_per_day, population_size):
    # Başlangıç popülasyonunu oluştur
    population = create_initial_population(doctors, days=days, shifts_per_day=shifts_per_day, population_size=population_size)

    # Her schedule için fitness puanını hesapla ve tut
    population_with_fitness_score = []
    for schedule in population:
        fitness_score = calculate_fitness(schedule, doctors, doctor_mapping)
        population_with_fitness_score.append((schedule, fitness_score))

    population_with_fitness_score.sort(key=lambda x: x[1], reverse=True)


    # Elit bireyleri seç ve turnuva havuzunu oluştur
    next_generation_pool, tournament_pool = handle_elites(population_with_fitness_score)
   
    print("\n--- Next Generation Pool ---")
    for schedule, fitness_score in next_generation_pool:
        print(f"Fitness: {fitness_score}")

    print("\n--- Tournament Pool ---")
    for schedule, fitness_score in tournament_pool:
        print(f"Fitness: {fitness_score}")

    # Turnuva havuzunda eleme yap
    filtered_tournament_pool = random_preselect_tournament_pool(tournament_pool)

    # Eleme sonrası bireyler arasında eşleşme yaparak parent havuzunu oluştur
    parent_pool = create_parent_pool_from_pairs(filtered_tournament_pool)

    print("\n--- Parent Pool ---")
    for schedule, fitness_score in parent_pool:
        print(f"Fitness: {fitness_score}")