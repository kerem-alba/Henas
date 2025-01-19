import random
from config.algorithm_config import mr, mi, doctor_swap_rate, shift_swap_rate, day_swap_rate, printOn
from genetic_algorithm.fitness.fitness_methods import calculate_fitness

def mutate_schedule(schedule):
    # Rastgele bir mutasyon türü seç
    mutation_type = random.choices(
        ["doctor_swap", "shift_swap", "day_swap"],
        weights=[0.5, 0.3, 0.2],  # Mutasyon oranları (örnek olarak verildi)
        k=1
    )[0]

    # Seçilen mutasyon türüne göre mutasyon uygula
    if mutation_type == "doctor_swap":
        return doctor_swap(schedule)
    elif mutation_type == "shift_swap":
        return shift_swap(schedule)
    elif mutation_type == "day_swap":
        return day_swap(schedule)

    # Eğer mutasyon türü seçilmezse (teknik olarak mümkün değil), orijinali döndür
    return schedule


def doctor_swap(schedule):
    # Rastgele iki gün seç
    day1_index, day2_index = random.sample(range(len(schedule)), 2)
    day1, day2 = schedule[day1_index], schedule[day2_index]

    # Rastgele iki shift seç
    shift1_index = random.randint(0, len(day1) - 1)
    shift2_index = random.randint(0, len(day2) - 1)
    shift1, shift2 = day1[shift1_index], day2[shift2_index]

    # Rastgele iki doktorun indeksini seç
    idx1 = random.randint(0, len(shift1) - 1)
    idx2 = random.randint(0, len(shift2) - 1)

    doctor1 = shift1[idx1]
    doctor2 = shift2[idx2]
    log_entry = (
        f"Swap Attempt: Day {day1_index + 1}, Shift {shift1_index + 1}, Doctor {doctor1} "
        f"<--> Day {day2_index + 1}, Shift {shift2_index + 1}, Doctor {doctor2}\n"
    )

    # Doktorları yer değiştir
    shift1[idx1], shift2[idx2] = shift2[idx2], shift1[idx1]

    with open("generation_log.txt", "a") as log_file:
        log_file.write(log_entry)

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