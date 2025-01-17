from config.algorithm_config import hard_penalty
from services.database_service import get_seniority_levels

# Hard Constraint 1: Aynı shift içinde aynı doktor birden fazla kez atanmış mı?
def check_duplicate_shifts(schedule):
    penalty = 0
    for day_index, day in enumerate(schedule):
        for shift_index, shift in enumerate(day):
            if len(shift) != len(set(shift)):
                duplicates = {doctor_code for doctor_code in shift if shift.count(doctor_code) > 1}
                penalty += hard_penalty * len(duplicates)
                #print(f"Penalty applied: Duplicate doctor(s) in Shift {shift_index + 1} on Day {day_index + 1}")
    return penalty

# Hard Constraint 2: Ardışık günlerde aynı doktora shift atanmış mı?
def check_consecutive_shifts(schedule):
    penalty = 0
    for day_index, day in enumerate(schedule):
        for shift_index, shift in enumerate(day):
            if shift_index > 0:
                for doctor_code in shift:
                    if doctor_code in day[shift_index - 1]:
                        penalty += hard_penalty
                        #print(f"Penalty applied: Doctor {doctor_code} assigned to consecutive shifts on Day {day_index + 1}")
            if shift_index == 1 and day_index < len(schedule) - 1:
                for doctor_code in shift:
                    if doctor_code in schedule[day_index + 1][0]:
                        penalty += hard_penalty
                        #print(f"Penalty applied: Doctor {doctor_code} assigned to night shift on Day {day_index + 1} and day shift on Day {day_index + 2}")
    return penalty

# Hard Constraint 3: 2 geceden fazla üst üste nöbet kontrolü
def check_three_consecutive_night_shifts(schedule):
    penalty = 0
    for day_index in range(len(schedule) - 2):
        night_shift_1 = schedule[day_index][1]
        night_shift_2 = schedule[day_index + 1][1]
        night_shift_3 = schedule[day_index + 2][1]
        for doctor_code in night_shift_1:
            if doctor_code in night_shift_2 and doctor_code in night_shift_3:
                penalty += hard_penalty
                #print(f"Penalty applied: Doctor {doctor_code} assigned to 3 consecutive night shifts starting from Day {day_index + 1}")
    return penalty

# Hard Constraint: Her shiftte her kıdemden en az bir doktor var mı?
def check_coverage_in_shift(schedule, doctors):
    penalty = 0
    seniority_levels = get_seniority_levels()

    for day_index, day in enumerate(schedule):
        for shift_index, shift in enumerate(day):
            # Shiftteki doktorların kıdemlerini hesapla
            shift_seniorities = set()
            for doctor_code in shift:
                doctor = next((d for d in doctors if d.code == doctor_code), None)
                if doctor:
                    shift_seniorities.add(doctor.seniority)

            # Eksik kıdem seviyelerini belirle
            missing_levels = seniority_levels - shift_seniorities
            if missing_levels:
                penalty += hard_penalty * len(missing_levels)  # Eksik kıdem başına ceza
                #print(f"Penalty applied: Missing seniority levels {missing_levels} in Shift {shift_index + 1} on Day {day_index + 1}.")

    return penalty

