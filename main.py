from models.doctor import Doctor
from utils.helpers import assign_codes, create_initial_population, update_shift_counts_by_name
from services.database_service import get_doctors

# Veritabanından doktor verilerini çek
doctor_data = get_doctors()
doctors = [Doctor(None, name, seniority, shift_count) for name, seniority, shift_count in doctor_data]

# Doktor kodlarını ata
doctors = assign_codes(doctors)

# Nöbet sayısı güncellemeleri (isimlere göre)
from config.shift_updates import shift_updates
doctors = update_shift_counts_by_name(doctors, shift_updates)

# Başlangıç popülasyonunu oluştur
population = create_initial_population(doctors, days=30, shifts_per_day=2, population_size=5)

# Her schedule'da doktorların kaç kez nöbete atandığını say
def count_shifts_per_schedule(population):
    shift_counts_per_schedule = []

    for schedule_index, schedule in enumerate(population):
        doctor_shift_counts = {}
        for day in schedule:
            for shift in day:
                for doctor_code in shift:
                    if doctor_code in doctor_shift_counts:
                        doctor_shift_counts[doctor_code] += 1
                    else:
                        doctor_shift_counts[doctor_code] = 1
        shift_counts_per_schedule.append(doctor_shift_counts)

    return shift_counts_per_schedule

# Tüm schedule'lardaki nöbet sayısını kontrol et ve yazdır
shift_counts_per_schedule = count_shifts_per_schedule(population)

for doctor in doctors:
    assigned_shifts = []
    for schedule_index, shift_counts in enumerate(shift_counts_per_schedule):
        shifts_in_schedule = shift_counts.get(doctor.code, 0)
        assigned_shifts.append(f"Schedule {schedule_index + 1}: {shifts_in_schedule}")
    
    print(
        f"Doctor: {doctor.name}, Code: {doctor.code}, Assigned Shifts: {', '.join(assigned_shifts)}, Expected Shifts per schedule: {doctor.shift_count}"
    )
