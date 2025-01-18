import random
import math
from config.algorithm_config import e, etr, tr

def handle_elites(population_with_fitness_score):
    next_generation_pool = []  # Gelecek nesil havuzu
    tournament_pool = []  # Turnuva havuzu

    # Elit bireyleri seç (en yüksek fitness'a sahip ilk 'elite_count' birey)
    elites = population_with_fitness_score[:e]
    
    # Elit bireyleri etr olasılığına göre yeni nesil havuzuna ekle
    for elite in elites:
        if random.random() <= etr:
            next_generation_pool.append(elite)  # Elit birey doğrudan yeni nesle geçer
        else:
            tournament_pool.append(elite)  # Geçmeyen birey turnuva havuzuna eklenir

    # Geriye kalan bireyleri turnuva havuzuna ekle
    tournament_pool += population_with_fitness_score[e:]

    return next_generation_pool, tournament_pool


def random_preselect_tournament_pool(tournament_pool):
    filtered_size = math.ceil(tr * len(tournament_pool))
    
    # Rastgele birey seç
    filtered_pool = random.sample(tournament_pool, filtered_size)
    return filtered_pool

def create_parent_pool_from_pairs(filtered_pool):
    parent_pool = []

    # Turnuva havuzundaki bireyleri karıştır
    random.shuffle(filtered_pool)

    # İkili eşleşme yap
    for i in range(0, len(filtered_pool) - 1, 2):
        # Eşleşen iki birey
        individual1 = filtered_pool[i]
        individual2 = filtered_pool[i + 1]

        # Daha yüksek fitness değerine sahip bireyi parent havuzuna ekle
        winner = individual1 if individual1[1] > individual2[1] else individual2
        parent_pool.append(winner)

    # Eğer havuzda tek birey kaldıysa, bu bireyi doğrudan parent havuzuna ekle
    if len(filtered_pool) % 2 == 1:
        parent_pool.append(filtered_pool[-1])

    return parent_pool



