from config.algorithm_config import (
    penalty_unequal_day_night_shifts,
    penalty_two_night_shifts,
    penalty_weekend_free,
    penalty_hierarchy_mismatch,
    week_start_day,
    penalty_shift_on_leave,
    hard_penalty,
)
import config.globals as g


def check_unequal_day_night_shifts(schedule, log):
    penalty = 0
    doctor_shift_counts = {}

    for day in schedule:
        day_shift = day[0]  # Gündüz shift
        night_shift = day[1]  # Gece shift

        for doctor in day_shift:
            doctor_shift_counts[doctor] = doctor_shift_counts.get(
                doctor, {"day": 0, "night": 0}
            )
            doctor_shift_counts[doctor]["day"] += 1

        for doctor in night_shift:
            doctor_shift_counts[doctor] = doctor_shift_counts.get(
                doctor, {"day": 0, "night": 0}
            )
            doctor_shift_counts[doctor]["night"] += 1

    for doctor, shifts in doctor_shift_counts.items():
        shift_difference = shifts["night"] - shifts["day"]
        if shift_difference > 0:
            penalty += (shift_difference) * penalty_unequal_day_night_shifts
            if log:
                with open("generation_log.txt", "a") as log_file:
                    log_file.write(
                        f"Doctor {doctor} has an unequal day-night shift distribution: "
                        f"{shifts['day']} day shifts and {shifts['night']} night shifts. "
                    )

    return penalty


def check_two_night_shifts(schedule, log):
    penalty = 0
    doctor_night_shifts = {}

    # Her doktorun gece nöbetlerini gün gün kontrol et
    for day_index, day in enumerate(schedule):
        night_shift = day[1]  # Gece shift

        for doctor in night_shift:
            if doctor not in doctor_night_shifts:
                doctor_night_shifts[doctor] = []

            doctor_night_shifts[doctor].append(day_index)

    # Doktorların gece nöbetlerini kontrol et
    for doctor, night_days in doctor_night_shifts.items():
        for i in range(len(night_days) - 1):
            if night_days[i + 1] == night_days[i] + 1:  # 2 gece üst üste kontrolü
                penalty += penalty_two_night_shifts
                if log:
                    with open("generation_log.txt", "a") as log_file:
                        log_file.write(
                            f"Doctor {doctor} assigned to 2 consecutive night shifts on Day {night_days[i] + 1} and Day {night_days[i + 1] + 1}\n"
                        )
    return penalty


def check_weekend_free(schedule, doctors, log):

    penalty = 0

    # Her doktorun nöbet tuttuğu günleri takip et
    doctor_shifts = {doctor.code: set() for doctor in doctors}

    # Programdaki nöbetleri kontrol et
    for day_index, day in enumerate(schedule):
        for shift in day:
            for doctor in shift:
                doctor_shifts[doctor].add(day_index)

    # Haftanın günlerini düzenle
    total_days = len(schedule)
    weekend_days = [
        (week_start_day + 5) % 7,
        (week_start_day + 6) % 7,
    ]  # Cumartesi ve Pazar günleri

    # Her doktorun hafta sonu boş olup olmadığını kontrol et
    for doctor, shifts in doctor_shifts.items():
        has_free_weekend = False

        # Tüm hafta sonlarını kontrol et
        for i in range(0, total_days, 7):  # Her hafta başlangıcı
            saturday = i + weekend_days[0]
            sunday = i + weekend_days[1]

            if saturday < total_days and sunday < total_days:
                if saturday not in shifts and sunday not in shifts:
                    has_free_weekend = True
                    break

        # Eğer hiç boş hafta sonu yoksa ceza uygula
        if not has_free_weekend:
            penalty += penalty_weekend_free
            if log:
                with open("generation_log.txt", "a") as log_file:
                    log_file.write(f"Doctor {doctor} has no completely free weekend.\n")
    return penalty


def check_hierarchy_mismatch(schedule, doctors, log):
    penalty = 0
    doctor_dict = {doctor.code: doctor for doctor in doctors}

    min_doctors_per_area = {
        info["id"]: info["min_doctors_per_area"] for area, info in g.shift_areas_data.items()
    }


    for day_index, day in enumerate(schedule):
        for shift_index, shift in enumerate(day):

            # 1) Birincil alana göre alan sayıları
            primary_counts = {area: 0 for area in min_doctors_per_area.keys()}
            # 2) İkincil alanda kaç doktor bu alana kayabilir?
            secondary_counts = {area: 0 for area in min_doctors_per_area.keys()}

            # Doktorları inceleyip sayıları doldur
            for doctor_code in shift:
                doctor = doctor_dict.get(doctor_code)
                if not doctor or not doctor.shift_areas:
                    continue
                
                # Birincil alan
                primary_area = doctor.shift_areas[0]
                if primary_area in primary_counts:
                    primary_counts[primary_area] += 1

                # Eğer ikincil alanı varsa, oraya kayma potansiyelini de say
                if len(doctor.shift_areas) > 1:
                    secondary_area = doctor.shift_areas[1]
                    if secondary_area in secondary_counts:
                        secondary_counts[secondary_area] += 1

            # 3) Eksikleri hesapla
            for area, required_count in min_doctors_per_area.items():
                current_count = primary_counts.get(area, 0)
                missing = required_count - current_count

                # Eğer eksik yoksa devam et
                if missing <= 0:
                    continue

                if log:
                    with open("generation_log.txt", "a") as log_file:
                        log_file.write(
                            f"Day {day_index + 1}, Shift {shift_index + 1}: Missing {missing} doctors in Area {area}.\n"
                        )

                # 4) Eksik alanı, ikincil alan ile kapatmaya çalış
                can_fill = secondary_counts.get(area, 0)

                # İkincil alan ile karşılanabilecek kısım
                fill = min(missing, can_fill)
                if fill > 0:
                    penalty += fill * penalty_hierarchy_mismatch
                    missing -= fill
                    if log:
                        with open("generation_log.txt", "a") as log_file:
                            log_file.write(
                                f"Filled {fill} missing doctors in Area {area} using secondary areas. Penalty added: {fill * penalty_hierarchy_mismatch}.\n"
                            )

                # 5) Hâlâ eksik varsa hard_penalty ekle
                if missing > 0:
                    penalty += missing * hard_penalty
                    if log:
                        with open("generation_log.txt", "a") as log_file:
                            log_file.write(
                                f"Hard penalty applied for {missing} remaining missing doctors in Area {area}. Penalty added: {missing * hard_penalty}.\n"
                            )

    return penalty


def check_leave_days(schedule, doctors, log):

    penalty = 0

    for day_index, day in enumerate(schedule):
        for shift_index, shift in enumerate(day):
            for doctor_code in shift:
                # Doktor bilgisi varsa izinleri kontrol et
                doctor = next((doc for doc in doctors if doc.code == doctor_code), None)
                if not doctor:
                    continue

                # Optional izin ihlali
                if [day_index + 1, shift_index] in doctor.optional_leaves:
                    penalty += penalty_shift_on_leave
                    if log:
                        with open("generation_log.txt", "a") as log_file:
                            log_file.write(
                                f"Day {day_index + 1}, Shift {shift_index}: Doctor {doctor_code} has an optional leave but assigned to a shift. Soft penalty: {penalty_shift_on_leave}.\n"
                            )

                # Mandatory izin ihlali
                if [day_index + 1, shift_index] in doctor.mandatory_leaves:
                    penalty += hard_penalty
                    if log:
                        with open("generation_log.txt", "a") as log_file:
                            log_file.write(
                                f"Day {day_index + 1}, Shift {shift_index}: Doctor {doctor_code} has a mandatory leave but assigned to a shift. Hard penalty: {hard_penalty}.\n"
                            )

    return penalty
