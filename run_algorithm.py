from models.doctor import Doctor
from genetic_algorithm.genetic_algorithm import run_genetic_algorithm
from hill_climbing_algorithm.hill_climbing_algorithm import run_hill_climbing
import time


def run_algorithm(doctor_data):
    doctors = [
        Doctor(
            doc["code"],
            doc["name"],
            doc["seniority_id"],
            doc["shift_count"],
            doc["shift_areas"],
            doc["optional_leaves"],
            doc["mandatory_leaves"],
        )
        for doc in doctor_data
    ]

    start_time = time.perf_counter()

    # run_genetic_algorithm(doctors)
    population = run_hill_climbing(doctors)

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    print(
        f"run_genetic_algorithm completed in {int(minutes)} minutes and {seconds:.2f} seconds"
    )

    return population
