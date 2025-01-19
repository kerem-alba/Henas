from config.algorithm_config import hard_penalty
from services.database_service import get_seniority_levels
from collections import Counter

# Hard Constraint 1: Aynı shift içinde aynı doktor birden fazla kez atanmış mı?
def check_duplicate_shifts(schedule):
    penalty = 0
    for day_index, day in enumerate(schedule):
        for shift_index, shift in enumerate(day):
            freq = Counter(shift)
            for doctor_code, count in freq.items():
                if count > 1:
                    penalty += hard_penalty * (count - 1)
                    #print(f"Penalty for {doctor_code} x{count} in Shift {shift_index+1} on Day {day_index+1}")
    return penalty

# Hard Constraint 2: Ardışık günlerde aynı doktora shift atanmış mı?
def check_consecutive_shifts(schedule):
    penalty = 0
    for day_index in range(len(schedule)):
        day = schedule[day_index]
        for shift_index in range(len(day) - 1):
            # Aynı gün içinde ardışık shift (day i, shift j) ile (day i, shift j+1)
            current_shift = day[shift_index]
            next_shift = day[shift_index + 1]
            for doctor_code in current_shift:
                if doctor_code in next_shift:
                    penalty += hard_penalty

            # Ardışık gün kontrolü (day i, shift j+1) ile (day i+1, shift j)
            if day_index < len(schedule) - 1:
                next_day_shift = schedule[day_index + 1][shift_index]
                for doctor_code in next_shift:
                    if doctor_code in next_day_shift:
                        penalty += hard_penalty

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

