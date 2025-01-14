from algorithms.initial_population import create_initial_population
from algorithms.fitness_calculator import calculate_fitness

def run_genetic_algorithm(doctors, days, shifts_per_day, population_size):
    # Başlangıç popülasyonunu oluştur
    population = create_initial_population(doctors, days=days, shifts_per_day=shifts_per_day, population_size=population_size)

    # Her schedule için fitness puanını hesapla ve yazdır
    print("\n--- Fitness Scores ---")
    for i, schedule in enumerate(population):
        fitness_score = calculate_fitness(schedule, doctors)
        print(f"Schedule {i + 1}: Fitness Score = {fitness_score}")
