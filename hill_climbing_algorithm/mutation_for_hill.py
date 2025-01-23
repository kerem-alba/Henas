import random
from config.algorithm_config import printOn, min_doctors_per_shift, max_doctors_per_shift

def mutate_schedule(schedule, doc_rate, slide_rate, shift_rate, day_rate):
    # Rastgele bir mutasyon türü seç
    mutation_type = random.choices(
        ["doctor_swap", "doctor_slide", "shift_swap", "day_swap"],
        weights=[doc_rate, slide_rate,  shift_rate, day_rate],
        k=1
    )[0]

    # Seçilen mutasyon türüne göre mutasyon uygula
    if mutation_type == "doctor_swap":
        return doctor_swap(schedule)
    elif mutation_type == "doctor_slide":
        return doctor_slide(schedule)
    elif mutation_type == "shift_swap":
        return shift_swap(schedule)
    elif mutation_type == "day_swap":
        return day_swap(schedule)

    # Eğer mutasyon türü seçilmezse (teknik olarak mümkün değil), orijinali döndür



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
        f"Doctor Swap Attempt: Day {day1_index + 1}, Shift {shift1_index + 1}, Doctor {doctor1} "
        f"<--> Day {day2_index + 1}, Shift {shift2_index + 1}, Doctor {doctor2}\n"
    )

    # Doktorları yer değiştir
    shift1[idx1], shift2[idx2] = shift2[idx2], shift1[idx1]

    with open("generation_log.txt", "a") as log_file:
        log_file.write(log_entry)

    return schedule

def doctor_slide(schedule):
    while True:  
        day_from = random.randint(0, len(schedule) - 1)
        shift_from = random.randint(0, len(schedule[day_from]) - 1)

        if len(schedule[day_from][shift_from]) > min_doctors_per_shift:
            break
    while True:
        day_to = random.randint(0, len(schedule) - 1)
        shift_to = random.randint(0, len(schedule[day_to]) - 1)

        if len(schedule[day_to][shift_to]) <= max_doctors_per_shift:
            break

    doctor_to_slide = random.choice(schedule[day_from][shift_from])
    schedule[day_from][shift_from].remove(doctor_to_slide)
    schedule[day_to][shift_to].append(doctor_to_slide)

    log_entry = (
        f"Doctor Slide Attempt: Doctor {doctor_to_slide} to move from "
        f"Day {day_from + 1}, Shift {shift_from + 1} "
        f"to Day {day_to + 1}, Shift {shift_to + 1}\n"
    )

    with open("generation_log.txt", "a") as log_file:
        log_file.write(log_entry)

    return schedule

def shift_swap(schedule):
    # Rastgele iki gün seç
    day1_index, day2_index = random.sample(range(len(schedule)), 2)
    day1, day2 = schedule[day1_index], schedule[day2_index]

    # Rastgele iki shift seç
    shift1_index = random.randint(0, len(day1) - 1)
    shift2_index = random.randint(0, len(day2) - 1)

    log_entry = (
        f"Shift Swap Attempt: Day {day1_index + 1}, Shift {shift1_index + 1} "
        f"<--> Day {day2_index + 1}, Shift {shift2_index + 1}\n"
    )

    # İki shift'i yer değiştir
    day1[shift1_index], day2[shift2_index] = day2[shift2_index], day1[shift1_index]

    if printOn:
        print("Shift Swap Mutation Applied")

    with open("generation_log.txt", "a") as log_file:
        log_file.write(log_entry)

    return schedule


def day_swap(schedule):
    """İki günü tamamen yer değiştirir."""
    idx1, idx2 = random.sample(range(len(schedule)), 2)  # İki günün indeksini seç
    schedule[idx1], schedule[idx2] = schedule[idx2], schedule[idx1]  # Yer değiştir

    log_entry = (
        f"Day Swap Attempt: Day {idx1 + 1} "
        f"<--> Day {idx2 + 1}, Shift\n"
    )

    if printOn:
        print("Day Swap Mutation Applied")

    with open("generation_log.txt", "a") as log_file:
        log_file.write(log_entry)

    return schedule