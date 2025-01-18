# Algoritma Parametreleri
population_size = 10
days = 30
shifts_per_day = 2

e = 1 # Elitist count
etr = 0.8 # Elit transfer rate
tr = 0.8 # Tournament attendance rate
ps = "random" # Parent pairing strategy
shuffle_sequential = False # Parent pairing shuffle sequential
cr = 0.9 # Crossover rate
mr = 0.2 # Mutation rate
doctor_swap_rate = 0.5 # Doctor swap rate
shift_swap_rate = 0.3 # Shift swap rate
day_swap_rate = 0.2 # Day swap rate

initial_fitness_score = 1000  # Başlangıç puanı

# Hard penalty
hard_penalty = 1000

# Soft penalties
penalty_unequal_day_night_shifts = 10  # Gündüz-gece farkı cezası
penalty_weekend_free = 50  # Haftasonu boş olmama cezası
penalty_two_night_shifts = 20  # 2 gece üst üste nöbet cezası
penalty_hierarchy_mismatch = 40  # Nöbet alanındaki hiyerarşi hatası cezası
