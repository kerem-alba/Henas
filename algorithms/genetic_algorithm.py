from algorithms.initial_population import create_initial_population
from algorithms.fitness.fitness_methods import calculate_fitness
from algorithms.selection.parent_selection_methods import handle_elites, random_preselect_tournament_pool, create_parent_pool_from_pairs
from algorithms.selection.crossover_methods import pair_parents, generate_next_generation_with_pmx
from algorithms.mutation.mutation_methods import apply_mutation

def run_genetic_algorithm(
    doctors, doctor_mapping, days, shifts_per_day, population_size, max_generations=500
):
    # Başlangıç popülasyonunu oluştur
    population = create_initial_population(
        doctors, days=days, shifts_per_day=shifts_per_day, population_size=population_size
    )
    # Başlangıç popülasyonunun fitness puanlarını hesapla ve yazdır
    population_with_fitness_score = [
        (schedule, calculate_fitness(schedule, doctors, doctor_mapping)) for schedule in population
    ]
    population_with_fitness_score.sort(key=lambda x: x[1], reverse=True)

    print("\n--- Initial Population Fitness Scores ---")
    total_fitness_initial = 0
    for i, (_, fitness_score) in enumerate(population_with_fitness_score, start=1):
        print(f"Schedule {i}: Fitness = {fitness_score}")
        total_fitness_initial += fitness_score
    print(f"Total Fitness (Initial Population): {total_fitness_initial}")

    for generation in range(1, max_generations + 1):
        # Her schedule için fitness puanını hesapla ve tut
        population_with_fitness_score = [
            (schedule, calculate_fitness(schedule, doctors, doctor_mapping)) for schedule in population
        ]
        population_with_fitness_score.sort(key=lambda x: x[1], reverse=True)

        # Elit bireyleri seç ve turnuva havuzunu oluştur
        next_generation_pool, tournament_pool = handle_elites(population_with_fitness_score)

        # Turnuva havuzunda eleme yap
        filtered_tournament_pool = random_preselect_tournament_pool(tournament_pool)

        # Eleme sonrası bireyler arasında eşleşme yaparak parent havuzunu oluştur
        parent_pool = create_parent_pool_from_pairs(filtered_tournament_pool)

        # Çaprazlama
        pairs = pair_parents(parent_pool)
        next_generation_pool = generate_next_generation_with_pmx(pairs, next_generation_pool)

        # Mutasyon uygula
        next_generation_pool = apply_mutation(next_generation_pool)

        # Yeni nesil fitness hesaplaması
        next_generation_with_fitness = [
            (schedule, calculate_fitness(schedule, doctors, doctor_mapping)) for schedule, _ in next_generation_pool
        ]

        # Toplam fitness hesapla
        total_fitness = sum(fitness_score for _, fitness_score in next_generation_with_fitness)

        # Tüm bireylerin fitness puanlarını yazdır
        print(f"\n--- Generation {generation}: Fitness Scores ---")
        for i, (_, fitness_score) in enumerate(next_generation_with_fitness, start=1):
            print(f"Schedule {i}: Fitness = {fitness_score}")

        # Toplam fitness puanını yazdır
        print(f"Total Fitness (Generation {generation}): {total_fitness}")

        # Bir sonraki nesil için popülasyonu ayarla
        population = [schedule for schedule, _ in next_generation_with_fitness]

    print("\n=== Algorithm Completed ===")
