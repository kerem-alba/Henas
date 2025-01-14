from services.database_service import get_doctors
from models.doctor import Doctor
from algorithms.genetic_algorithm import run_genetic_algorithm
from config.algorithm_config import population_size, shifts_per_day, days
from utils.helpers import assign_codes, update_shift_counts_by_name
from config.shift_updates import shift_updates

# Veritabanından doktor verilerini çek
doctor_data = get_doctors()
print(doctor_data)
doctors = [Doctor(None, name, seniority, shift_count, shift_areas) for name, seniority, shift_count, shift_areas in doctor_data]

# Doktor kodlarını ata
doctors = assign_codes(doctors)

# Nöbet sayısı güncellemeleri (isimlere göre)
doctors = update_shift_counts_by_name(doctors, shift_updates)
print(doctors)

# Genetik algoritmayı çalıştır
run_genetic_algorithm(doctors, days=days, shifts_per_day=shifts_per_day, population_size=population_size)





