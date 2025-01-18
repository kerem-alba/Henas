from services.database_service import get_doctors
from models.doctor import Doctor
from algorithms.genetic_algorithm import run_genetic_algorithm
from config.algorithm_config import population_size, shifts_per_day, days
from utils.helpers import assign_codes, update_shift_counts_by_name
from config.shift_updates import shift_updates
import time

# Veritabanından doktor verilerini çek
doctor_data = get_doctors()
doctors = [Doctor(None, name, seniority, shift_count, shift_areas) for name, seniority, shift_count, shift_areas in doctor_data]
# Doktor kodlarını ata
doctors, doctor_mapping = assign_codes(doctors)

# Nöbet sayısı güncellemeleri (isimlere göre)
doctors = update_shift_counts_by_name(doctors, shift_updates)
print("Doctors:",doctors)


start_time = time.perf_counter()

# Genetik algoritmayı çalıştır
run_genetic_algorithm(doctors, doctor_mapping, days=days, shifts_per_day=shifts_per_day, population_size=population_size)

end_time = time.perf_counter()


elapsed_time = end_time - start_time
minutes, seconds = divmod(elapsed_time, 60)
print(f"run_genetic_algorithm completed in {int(minutes)} minutes and {seconds:.2f} seconds")


