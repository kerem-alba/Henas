from config.algorithm_config import penalty_unequal_day_night_shifts, penalty_two_night_shifts, penalty_weekend_free, penalty_hierarchy_mismatch
from services.database_service import get_doctor_seniority, get_doctor_mapping

def check_unequal_day_night_shifts(schedule):

    penalty = 0
    doctor_shift_counts = {}

    # Her doktorun nöbetlerini say
    for day in schedule:
        day_shift = day[0]  # Gündüz shift
        night_shift = day[1]  # Gece shift

        for doctor in day_shift:
            doctor_shift_counts[doctor] = doctor_shift_counts.get(doctor, {'day': 0, 'night': 0})
            doctor_shift_counts[doctor]['day'] += 1

        for doctor in night_shift:
            doctor_shift_counts[doctor] = doctor_shift_counts.get(doctor, {'day': 0, 'night': 0})
            doctor_shift_counts[doctor]['night'] += 1

    # Her doktorun gündüz-gece farkını kontrol et ve ceza hesapla
    for doctor, shifts in doctor_shift_counts.items():
        shift_difference = abs(shifts['day'] - shifts['night'])
        if shift_difference > 1:
            penalty += (shift_difference - 1) * penalty_unequal_day_night_shifts

    return penalty

def check_two_night_shifts(schedule):
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
                #print(f"Penalty applied: Doctor {doctor} assigned to 2 consecutive night shifts on Day {night_days[i] + 1} and Day {night_days[i + 1] + 1}")

    return penalty

def check_weekend_free(schedule, doctors):
    penalty = 0

    # Her doktorun nöbet tuttuğu günleri takip et
    doctor_shifts = {doctor.code: set() for doctor in doctors}

    # Programdaki nöbetleri kontrol et
    for day_index, day in enumerate(schedule):
        for shift in day:
            for doctor in shift:
                doctor_shifts[doctor].add(day_index)

    # Her doktorun hafta sonu boş olup olmadığını kontrol et
    for doctor, shifts in doctor_shifts.items():
        has_free_weekend = False

        # Tüm hafta sonlarını kontrol et (Cumartesi = 5. gün, Pazar = 6. gün vb.)
        for i in range(0, len(schedule), 7):  # Her hafta başlangıcı
            if i + 5 < len(schedule) and i + 6 < len(schedule):  # Cumartesi ve Pazar varsa
                if (i + 5 not in shifts) and (i + 6 not in shifts):
                    has_free_weekend = True
                    break

        # Eğer hiç boş hafta sonu yoksa ceza uygula
        if not has_free_weekend:
            penalty += penalty_weekend_free
            #print(f"Penalty applied: Doctor {doctor} has no completely free weekend.")

    return penalty


def check_hierarchy_mismatch(schedule, doctors, doctor_mapping):
    penalty = 0

    # Doktorların kıdem bilgilerini veritabanından çek
    seniority = get_doctor_seniority()
    print("Seniority Data:", seniority)
    print("Doctor Mapping:", doctor_mapping)

    # Doktor kodlarına göre kıdem seviyelerini oluştur
    doctor_seniorities = {d.code: seniority.get(d.name, float('inf')) for d in doctors}
    print("Doctor Seniorities by Code:", doctor_seniorities)

    # Programdaki nöbetleri kontrol et
    for day_index, day in enumerate(schedule):
        for shift_index, shift in enumerate(day):
            print(f"\nDay {day_index + 1}, Shift {shift_index + 1}: {shift}")

            # Her nöbetteki doktorların hiyerarşik seviyelerini al
            shift_seniorities = [doctor_seniorities.get(doctor, float('inf')) for doctor in shift]
            print("Shift Seniorities:", shift_seniorities)

            # En düşük hiyerarşik seviyeye sahip doktorun seviyesi
            min_seniority = min(shift_seniorities)
            print("Min Seniority:", min_seniority)

            # Daha yüksek seviyeli doktor atanmış mı?
            for doctor, level in zip(shift, shift_seniorities):
                if level > min_seniority:
                    penalty += penalty_hierarchy_mismatch
                    print(f"Penalty applied: Doctor {doctor} (Level {level}) assigned to Shift {shift_index + 1} on Day {day_index + 1} despite higher-level doctor presence.")

    print("Total Penalty:", penalty)
    return penalty


