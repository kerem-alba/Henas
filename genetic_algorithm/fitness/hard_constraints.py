from config.algorithm_config import hard_penalty
from config.shift_updates import min_doctors_per_area
from collections import Counter

# Hard Constraint 1: Aynı shift içinde aynı doktor birden fazla kez atanmış mı?
def check_duplicate_shifts(schedule, log):
    penalty = 0
    for day_index, day in enumerate(schedule):
        for shift_index, shift in enumerate(day):
            freq = Counter(shift)
            for doctor_code, count in freq.items():
                if count > 1:
                    penalty += hard_penalty * (count - 1)

                    if log:
                        with open("generation_log.txt", "a") as log_file:
                            log_file.write(
                                f"{doctor_code} has been assigned {count} times on Day {day_index + 1}, Shift {shift_index + 1}\n"
                            )
    return penalty

# Hard Constraint 2: Ardışık günlerde aynı doktora shift atanmış mı?
def check_consecutive_shifts(schedule, log):
    penalty = 0
    for day_index in range(len(schedule)):
        day = schedule[day_index]
        for shift_index in range(len(day) - 1):
            current_shift = day[shift_index]
            next_shift = day[shift_index + 1]
            for doctor_code in current_shift:
                if doctor_code in next_shift:
                    penalty += hard_penalty

                    if log:
                        with open("generation_log.txt", "a") as log_file:
                            log_file.write(
                                f"{doctor_code} has consecutive shifts on Day {day_index + 1}, Shift {shift_index + 1} and {shift_index + 2}\n"
                            )

            if day_index < len(schedule) - 1:
                next_day_shift = schedule[day_index + 1][shift_index]
                for doctor_code in next_shift:
                    if doctor_code in next_day_shift:
                        penalty += hard_penalty
                        if log:
                            with open("generation_log.txt", "a") as log_file:
                                log_file.write(
                                    f"{doctor_code} has a shift on consecutive days: Day {day_index + 1} (Shift {shift_index + 2}) and Day {day_index + 2} (Shift {shift_index + 1})\n"
                                )

    return penalty



# Hard Constraint 3: 2 geceden fazla üst üste nöbet kontrolü
def check_three_consecutive_night_shifts(schedule, log):
    penalty = 0
    for day_index in range(len(schedule) - 2):
        night_shift_1 = schedule[day_index][1]
        night_shift_2 = schedule[day_index + 1][1]
        night_shift_3 = schedule[day_index + 2][1]
        for doctor_code in night_shift_1:
            if doctor_code in night_shift_2 and doctor_code in night_shift_3:
                penalty += hard_penalty
                if log:
                    with open("generation_log.txt", "a") as log_file:
                        log_file.write(
                            f"Doctor {doctor_code} assigned to 3 consecutive night shifts starting from Day {day_index + 1}\n"
                        )
    return penalty
