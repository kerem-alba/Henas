from config.algorithm_config import hard_penalty, min_doctors_per_area
from services.database_service import get_shift_areas

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

# Hard Constraint 4: Her nöbet alanında nöbet tutabilecek min doktor var mı?
def check_coverage_in_shift(schedule, doctors):
    penalty = 0
    shift_area_mapping = get_shift_areas()  # İsim -> ID eşlemesi
    required_areas = set(min_doctors_per_area.keys())  # Minimum gereksinim olan alanlar

    for day_index, day in enumerate(schedule):
        for shift_index, shift in enumerate(day):
            area_counts = {area: 0 for area in required_areas}
            for doctor_code in shift:
                doctor = next((d for d in doctors if d.code == doctor_code), None)
                if doctor:
                    for area_name in doctor.shift_areas:
                        area_id = shift_area_mapping.get(area_name)  # İsmi ID'ye çevir
                        if area_id in area_counts:
                            area_counts[area_id] += 1

            #print(f"Day {day_index + 1}, Shift {shift_index + 1},Doctors: {shift}, Area Counts: {area_counts}")

            for area, min_count in min_doctors_per_area.items():
                if area_counts[area] < min_count:
                    penalty += hard_penalty * (min_count - area_counts[area])
                    #print(f"Penalty applied: Area {area} in Shift {shift_index + 1} on Day {day_index + 1} "f"does not meet minimum requirement ({min_count} required, {area_counts[area]} present).")

    return penalty
