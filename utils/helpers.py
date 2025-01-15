
def assign_codes(doctors):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    doctor_mapping = {}

    for index, doctor in enumerate(doctors):
        code = alphabet[index % len(alphabet)]
        doctor.code = code
        doctor_mapping[code] = doctor.name

    return doctors, doctor_mapping



def update_shift_counts_by_name(doctors, updates):
    for doctor in doctors:
        if doctor.name in updates:
            doctor.shift_count = updates[doctor.name]
    return doctors


