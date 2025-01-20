from config.algorithm_config import penalty_unequal_day_night_shifts, penalty_two_night_shifts, penalty_weekend_free, penalty_hierarchy_mismatch, week_start_day
from services.database_service import  get_shift_areas
from config.shift_updates import min_doctors_per_area

def check_unequal_day_night_shifts(schedule, log):
    penalty = 0
    doctor_shift_counts = {}

    for day in schedule:
        day_shift = day[0]  # Gündüz shift
        night_shift = day[1]  # Gece shift

        for doctor in day_shift:
            doctor_shift_counts[doctor] = doctor_shift_counts.get(doctor, {'day': 0, 'night': 0})
            doctor_shift_counts[doctor]['day'] += 1

        for doctor in night_shift:
            doctor_shift_counts[doctor] = doctor_shift_counts.get(doctor, {'day': 0, 'night': 0})
            doctor_shift_counts[doctor]['night'] += 1

    for doctor, shifts in doctor_shift_counts.items():
        shift_difference = abs(shifts['day'] - shifts['night'])
        if shift_difference > 1:
            penalty += (shift_difference - 1) * penalty_unequal_day_night_shifts
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
    weekend_days = [(week_start_day + 5) % 7, (week_start_day + 6) % 7]  # Cumartesi ve Pazar günleri

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
                    log_file.write(
                        f"Doctor {doctor} has no completely free weekend.\n"
                    )
    return penalty



def check_hierarchy_mismatch(schedule, doctors, doctor_mapping):
    penalty = 0

    # Doktorların kıdem bilgilerini ve alanlarını al
    shift_area_mapping = get_shift_areas()

    for day_index, day in enumerate(schedule):
        for shift_index, shift in enumerate(day):
            #print(f"\nDay {day_index + 1}, Shift {shift_index + 1}: {shift}")

            # Doktorların max_area_for_level değerlerini saymak için bir sayaç
            area_counts = {1: 0, 2: 0, 3: 0, 4: 0}

            for doctor_code in shift:
                doctor_name = doctor_mapping.get(doctor_code)
                doctor_data = next((d for d in doctors if d.name == doctor_name), None)
                if doctor_data:
                    # Doktorun alan isimlerini ID'lere çevir
                    doctor_area_ids = [shift_area_mapping[area] for area in doctor_data.shift_areas if area in shift_area_mapping]

                    # En yüksek uygun alan (id bazlı)
                    max_area_for_level = min(doctor_area_ids, default=None)

                    if max_area_for_level:
                        area_counts[max_area_for_level] += 1

            #print(f"Max Area Counts for Shift {shift_index + 1} on Day {day_index + 1}: {area_counts}")

            # Eksiklikleri ve kaydırmaları hesapla
            deficit_counts = {area: max(0, min_doctors_per_area[area] - area_counts[area]) for area in area_counts}
            #print(f"Deficit Counts for Shift {shift_index + 1} on Day {day_index + 1}: {deficit_counts}")

            # Alanlardaki kaydırmaları hesapla
            for area in sorted(min_doctors_per_area.keys(), reverse=True):  # En düşük alanlardan başlayarak
                while deficit_counts[area] > 0:  # Eksik doktorlar için kaydırma yapılacak
                    higher_area = area - 1
                    if higher_area >= 1 and area_counts[higher_area] > min_doctors_per_area[higher_area]:
                        # Kaydırma işlemi
                        area_counts[higher_area] -= 1
                        area_counts[area] += 1
                        deficit_counts[area] -= 1
                        penalty += penalty_hierarchy_mismatch
                        #print(f"Penalty applied: Doctor moved from Area {higher_area} to Area {area}.")
                    else:
                        # Kaydırma mümkün değilse döngüyü kır
                        #print(f"No more doctors available to move from Area {higher_area} to Area {area}. Breaking loop.")
                        break

    #print("Total Penalty:", penalty)
    return penalty
