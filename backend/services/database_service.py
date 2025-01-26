import psycopg2

# Veritabanı bağlantı bilgileri
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": 5432,
}


def get_detailed_doctors():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT d.name, d.seniority_id, s.max_shifts_per_month, array_agg(sa.id ORDER BY sa.id)
        FROM doctors d
        JOIN seniority s ON d.seniority_id = s.id
        JOIN LATERAL unnest(s.shift_area_ids) AS area_id ON true
        JOIN shift_areas sa ON sa.id = area_id
        GROUP BY d.id, d.name, d.seniority_id, s.max_shifts_per_month
        ORDER BY d.id
    """
    )
    result = cur.fetchall()

    doctors = []
    for row in result:
        name, seniority, shift_count, shift_areas = row
        doctors.append((name, seniority, shift_count, shift_areas))

    cur.close()
    conn.close()
    return doctors


def get_doctors():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, name, seniority_id
        FROM doctors
        ORDER BY id
    """
    )
    result = cur.fetchall()

    doctors = []
    for row in result:
        doctors.append({"id": row[0], "name": row[1], "seniority_id": row[2]})

    cur.close()
    conn.close()
    return doctors


def add_doctor(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO doctors (name, seniority_id) VALUES (%s, %s) RETURNING id",
        (data["name"], data["seniority_id"]),
    )
    new_id = cur.fetchone()[0]  # Yeni eklenen doktorun ID'sini al
    conn.commit()
    cur.close()
    conn.close()

    return new_id


def update_doctor(doctor_id, data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        "UPDATE doctors SET name = %s, seniority_id = %s WHERE id = %s",
        (data["name"], data["seniority_id"], doctor_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_doctor(doctor_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("DELETE FROM doctors WHERE id = %s", (doctor_id,))
    conn.commit()
    cur.close()
    conn.close()


def get_seniority():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Seniority tablosunu getir
    cur.execute(
        """
        SELECT id, seniority_name, max_shifts_per_month, shift_area_ids
        FROM seniority
        ORDER BY id
    """
    )
    result = cur.fetchall()

    seniority_list = []
    for row in result:
        seniority_list.append(
            {
                "id": row[0],
                "seniority_name": row[1],
                "max_shifts_per_month": row[2],
                "shift_area_ids": row[3],
            }
        )

    cur.close()
    conn.close()

    return seniority_list


def add_seniority(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO seniority (seniority_name, max_shifts_per_month, shift_area_ids) VALUES (%s, %s, %s) RETURNING id",
        (data["seniority_name"], data["max_shifts_per_month"], data["shift_area_ids"]),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return new_id


def update_seniority(seniority_id, data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        "UPDATE seniority SET seniority_name = %s, max_shifts_per_month = %s, shift_area_ids = %s WHERE id = %s",
        (
            data["seniority_name"],
            data["max_shifts_per_month"],
            data["shift_area_ids"],
            seniority_id,
        ),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_seniority(seniority_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("DELETE FROM seniority WHERE id = %s", (seniority_id,))
    conn.commit()
    cur.close()
    conn.close()


def get_shift_areas():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT id, area_name FROM shift_areas")
    shift_areas = {row[1]: row[0] for row in cur.fetchall()}

    cur.close()
    conn.close()

    return shift_areas


def add_shift_area(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO shift_areas (area_name) VALUES (%s) RETURNING id",
        (data["area_name"],),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return new_id


def update_shift_area(area_id, data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        "UPDATE shift_areas SET area_name = %s WHERE id = %s",
        (data["area_name"], area_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_shift_area(area_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("DELETE FROM shift_areas WHERE id = %s", (area_id,))
    conn.commit()
    cur.close()
    conn.close()
