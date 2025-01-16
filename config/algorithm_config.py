# Algoritma Parametreleri
population_size = 3
days = 30
shifts_per_day = 2

initial_fitness_score = 1000  # Başlangıç puanı

# Hard penalty
hard_penalty = 1000

# Soft penalties
penalty_unequal_day_night_shifts = 10  # Gündüz-gece farkı cezası
penalty_weekend_free = 100  # Haftasonu boş olmama cezası
penalty_two_night_shifts = 20  # 2 gece üst üste nöbet cezası
penalty_hierarchy_mismatch = 100  # Nöbet alanındaki hiyerarşi hatası cezası

# Hastane parametreleri
min_doctors_per_area = {
    1: 1,  
    2: 1, 
    3: 1, 
    4: 2   
}