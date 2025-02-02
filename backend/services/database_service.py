import psycopg2
from psycopg2.extras import Json  # JSON formatı için

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
    SELECT d.id, d.name, s.seniority_name
    FROM doctors d
    INNER JOIN seniority s ON d.seniority_id = s.id
    """
    )
    result = cur.fetchall()

    doctors = [
        {"id": row[0], "name": row[1], "seniority_name": row[2]}  # 'id' alanını ekledik
        for row in result
    ]

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


def update_all_doctors(data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for doctor in data:
            cur.execute(
                """
                UPDATE doctors
                SET name = %s,
                    seniority_id = %s
                WHERE id = %s
                """,
                (doctor["name"], doctor["seniority_id"], doctor["id"]),
            )

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("update_all_doctors fonksiyonunda hata:", e)  # <-- Hata detayını görmek için
        raise



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

def get_detailed_seniority():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # JSONB içindeki sıralamaya göre nöbet alanlarını sıralı döndür
    cur.execute(
        """
        SELECT s.id, s.seniority_name, s.max_shifts_per_month, 
               ARRAY_AGG(sa.area_name ORDER BY area_ids.ordinality) AS shift_area_names
        FROM seniority s
        LEFT JOIN LATERAL jsonb_array_elements_text(s.shift_area_ids) WITH ORDINALITY AS area_ids(area_id, ordinality) ON true
        LEFT JOIN shift_areas sa ON sa.id = area_ids.area_id::int  -- JSON'dan gelen değeri integer'a çevir
        GROUP BY s.id, s.seniority_name, s.max_shifts_per_month
        ORDER BY s.id
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
                "shift_area_names": row[3] if row[3] is not None else [],
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




import json

def update_all_seniorities(data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for seniority in data:
            cur.execute(
                """
                UPDATE seniority
                SET seniority_name = %s,
                    max_shifts_per_month = %s,
                    shift_area_ids = %s
                WHERE id = %s
                """,
                (
                    seniority["seniority_name"],
                    seniority["max_shifts_per_month"],
                    json.dumps(seniority["shift_area_ids"]),  # JSON olarak sakla
                    seniority["id"],
                ),
            )

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("update_all_seniorities fonksiyonunda hata:", e)
        raise



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


def update_all_shift_areas(data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for area in data:
            cur.execute(
                "UPDATE shift_areas SET area_name = %s WHERE id = %s",
                (area["area_name"], area["id"]),
            )

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("update_all_shift_areas fonksiyonunda hata:", e)  # Hata mesajını göster
        raise


def delete_shift_area(area_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("DELETE FROM shift_areas WHERE id = %s", (area_id,))
    conn.commit()
    cur.close()
    conn.close()
