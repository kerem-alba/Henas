from genetic_algorithm.initial_population import create_initial_population
from genetic_algorithm.fitness.fitness_methods import calculate_fitness
from genetic_algorithm.selection.parent_selection_methods import handle_elites, distribute_to_pools, append_parents_from_tournament_pool
from genetic_algorithm.selection.crossover_methods import pair_parents, generate_next_generation_with_pmx
from genetic_algorithm.mutation.mutation_methods import apply_mutation
from config.algorithm_config import max_generations


def run_genetic_algorithm(doctors, doctor_mapping):
    # Başlangıç popülasyonunu oluştur
    population = create_initial_population(doctors)
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
        next_generation_pool, pre_tournament_pool, parent_pool = handle_elites(population_with_fitness_score)

        # Turnuva havuzunu oluştur ve parent havuzuna ekle
        tournament_pool, parent_pool = distribute_to_pools(pre_tournament_pool, parent_pool)

        # Turnuva havuzundan parent havuzuna geçen bireyleri ekle
        parent_pool = append_parents_from_tournament_pool(tournament_pool, parent_pool)

        # Çaprazlama
        pairs = pair_parents(parent_pool, next_generation_pool)
        next_generation_pool = generate_next_generation_with_pmx(pairs, next_generation_pool)

        # Mutasyon uygula
        next_generation_pool = apply_mutation(next_generation_pool)

        # Yeni nesil fitness hesaplaması
        next_generation_with_fitness = [
            (schedule, calculate_fitness(schedule, doctors, doctor_mapping)) for schedule, _ in next_generation_pool
        ]

        # Toplam fitness hesapla
        total_fitness = sum(fitness_score for _, fitness_score in next_generation_with_fitness)

        sorted_next_generation = sorted(next_generation_with_fitness, key=lambda x: x[1], reverse=True)

        # Tüm bireylerin fitness puanlarını yazdır
        print(f"\n--- Generation {generation}: Fitness Scores ---")
        for i, (_, fitness_score) in enumerate(sorted_next_generation, start=1):
            print(f"Schedule {i}: Fitness = {fitness_score}")

        # Toplam fitness puanını yazdır
        print(f"Total Fitness (Generation {generation}): {total_fitness}")

        # Bir sonraki nesil için popülasyonu ayarla
        population = [schedule for schedule, _ in next_generation_with_fitness]

    print("\n=== Algorithm Completed ===")
    
    # Tüm schedule'ları ve fitness puanlarını yazdır
    print("\n--- Final Generation: All Schedules and Fitness Scores ---")
    for i, (schedule, fitness_score) in enumerate(sorted_next_generation, start=1):
        print(f"Schedule {i}: Fitness = {fitness_score}")
        print("Schedule Structure:")
        for day in schedule:
            print(day)
        print("-" * 50)
