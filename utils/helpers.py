from models.doctor import Doctor
import random

def assign_codes(doctors):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for index, doctor in enumerate(doctors):
        doctor.code = alphabet[index % len(alphabet)]
    return doctors

def create_initial_population(doctors, days, shifts_per_day, population_size):
    population = []

    # Her doktorun kodunu nöbet sayısına göre listele ve karıştır
    temp_list = [doctor.code for doctor in doctors for _ in range(doctor.shift_count)]
    random.shuffle(temp_list)

    total_shifts = days * shifts_per_day

    for _ in range(population_size):
        schedule = [[[] for _ in range(shifts_per_day)] for _ in range(days)]

        for index, doctor_code in enumerate(temp_list):
            day = (index // shifts_per_day) % days
            shift_type = index % shifts_per_day
            schedule[day][shift_type].append(doctor_code)

        population.append(schedule)

    return population



def update_shift_counts_by_name(doctors, updates):
    for doctor in doctors:
        if doctor.name in updates:
            doctor.shift_count = updates[doctor.name]
    return doctors
