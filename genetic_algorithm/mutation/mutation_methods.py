import random
from config.algorithm_config import mr, mi, doctor_swap_rate, shift_swap_rate, day_swap_rate, printOn

def mutate_schedule(schedule):
    for _ in range(mi):
        mutation_type = random.choices(
            ["doctor_swap", "shift_swap", "day_swap"], 
            weights=[doctor_swap_rate, shift_swap_rate, day_swap_rate],
            k=1
        )[0]

        if mutation_type == "doctor_swap":
            schedule = doctor_swap(schedule)
        elif mutation_type == "shift_swap":
            schedule = shift_swap(schedule)
        elif mutation_type == "day_swap":
            schedule = day_swap(schedule)

    if printOn:
        print(f"Mutation Applied {mi} times")
    return schedule

def doctor_swap(schedule):
    # Rastgele iki gün seç
    day1, day2 = random.sample(schedule, 2)

    # Rastgele iki shift seç
    shift1 = random.choice(day1)
    shift2 = random.choice(day2)

    # Rastgele iki doktorun indeksini seç
    idx1 = random.randint(0, len(shift1) - 1)
    idx2 = random.randint(0, len(shift2) - 1)

    # Doktorları yer değiştir
    shift1[idx1], shift2[idx2] = shift2[idx2], shift1[idx1]
    if printOn:
        print("Doctor Swap Mutation Applied")

    return schedule


def shift_swap(schedule):
    # Rastgele iki gün seç
    day1, day2 = random.sample(schedule, 2)

    # Rastgele birer shift seç
    shift1 = random.choice(day1)
    shift2 = random.choice(day2)

    # İki shift'i yer değiştir
    idx1 = day1.index(shift1)
    idx2 = day2.index(shift2)
    day1[idx1], day2[idx2] = day2[idx2], day1[idx1]

    if printOn:
        print("Shift Swap Mutation Applied")

    return schedule

def day_swap(schedule):
    """İki günü tamamen yer değiştirir."""
    idx1, idx2 = random.sample(range(len(schedule)), 2)  # İki günün indeksini seç
    schedule[idx1], schedule[idx2] = schedule[idx2], schedule[idx1]  # Yer değiştir
    if printOn:
        print("Day Swap Mutation Applied")

    return schedule


def apply_mutation(next_generation_pool):
    mutated_pool = []
    for schedule, fitness_score in next_generation_pool:
        if random.random() <= mr:
            # Mutasyon yap
            mutated_schedule = mutate_schedule(schedule)
            mutated_pool.append((mutated_schedule, None))  # Fitness yeniden hesaplanacak
        else:
            # Mutasyon yok, olduğu gibi ekle
            mutated_pool.append((schedule, fitness_score))
    return mutated_pool
