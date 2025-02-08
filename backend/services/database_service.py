import psycopg2
import json


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
    ORDER BY d.id
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

    cur.execute(
        """
        SELECT s.id, s.seniority_name, s.max_shifts_per_month, 
               ARRAY_AGG(sa.area_name ORDER BY area_ids.ordinality) AS shift_area_names,
               ARRAY_AGG(area_ids.area_id::int ORDER BY area_ids.ordinality) AS shift_area_ids
        FROM seniority s
        LEFT JOIN LATERAL jsonb_array_elements_text(s.shift_area_ids) WITH ORDINALITY AS area_ids(area_id, ordinality) ON true
        LEFT JOIN shift_areas sa ON sa.id = area_ids.area_id::int
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
                "shift_area_ids": row[4] if row[4] is not None else []
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

    cur.execute("SELECT id, area_name, min_doctors_per_area  FROM shift_areas")
    shift_areas = {row[1]: {"id": row[0], "min_doctors_per_area": row[2]} for row in cur.fetchall()}

    cur.close()
    conn.close()

    return shift_areas


def add_shift_area(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO shift_areas (area_name, min_doctors_per_area) VALUES (%s, %s) RETURNING id",
        (data["area_name"], data["min_doctors_per_area"]),
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
                "UPDATE shift_areas SET area_name = %s, min_doctors_per_area = %s  WHERE id = %s",
                (area["area_name"], area["min_doctors_per_area"], area["id"]),
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

def get_schedule_data_by_id(schedule_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT schedule_data_name, schedule_data FROM schedule_data WHERE id = %s", (schedule_id,))
        row = cur.fetchone()

        schedule_data = {
            "name": row[0],
            "data": row[1]
        } if row else {}

        cur.close()
        conn.close()

        return schedule_data

    except Exception as e:
        print("get_schedule_data fonksiyonunda hata:", e)
        return {}

def get_all_schedule_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT id, schedule_data_name, schedule_data, created_at FROM schedule_data ORDER BY created_at DESC")
        rows = cur.fetchall()

        schedule_data = [
            {
                "id": row[0],
                "name": row[1],  
                "data": row[2], 
                "created_at": row[3]
            }
            for row in rows
        ]

        cur.close()
        conn.close()

        return schedule_data

    except Exception as e:
        print("get_schedule_data fonksiyonunda hata:", e)
        return []


def add_schedule_data(name, schedule_json):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO schedule_data (schedule_data_name, schedule_data) VALUES (%s, %s) RETURNING id",
            (name, json.dumps(schedule_json)),
        )
        
        schedule_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return {"message": "Nöbet listesi başarıyla kaydedildi.", "id": schedule_id}

    except Exception as e:
        print("save_schedule_data fonksiyonunda hata:", e)
        return {"error": "Bir hata oluştu."}
    
def delete_schedule_data(schedule_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("DELETE FROM schedule_data WHERE id = %s", (schedule_id,))
        conn.commit()

        cur.close()
        conn.close()

        return {"message": "Nöbet listesi başarıyla silindi."}

    except Exception as e:
        print("delete_schedule_data fonksiyonunda hata:", e)
        return {"error": "Silme işlemi sırasında bir hata oluştu."}


def update_schedule_data(schedule_id, new_name, new_schedule_json):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute(
            "UPDATE schedule_data SET schedule_data_name = %s, schedule_data = %s WHERE id = %s",
            (new_name, json.dumps(new_schedule_json), schedule_id)
        )
        
        conn.commit()

        cur.close()
        conn.close()

        return {"message": "Nöbet listesi başarıyla güncellendi."}

    except Exception as e:
        print("update_schedule_data fonksiyonunda hata:", e)
        return {"error": "Güncelleme işlemi sırasında bir hata oluştu."}



def get_schedule_by_id(schedule_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, schedule_data_id, schedule, fitness_score, log_messages, created_at 
        FROM schedules 
        WHERE id = %s
        """,
        (schedule_id,),
    )

    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        return {
            "id": result[0],
            "schedule_data_id": result[1],
            "schedule": result[2],
            "fitness_score": result[3],
            "log_messages": result[4],
            "created_at": result[5],
        }
    else:
        return None


def add_schedule(schedule_data_id, schedule):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute(
            """
            INSERT INTO schedules (schedule_data_id, schedule)
            VALUES (%s, %s)
            RETURNING id
            """,
            (schedule_data_id, json.dumps(schedule))  
        )
        
        schedule_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return schedule_id 

    except Exception as e:
        print("add_schedule fonksiyonunda hata:", e)
        return None

def add_fitness_score(schedule_id, fitness_score):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE schedules
            SET fitness_score = %s
            WHERE id = %s
            """,
            (fitness_score, schedule_id)
        )

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("add_fitness_score fonksiyonunda hata:", e)

import json
import psycopg2

import psycopg2

import psycopg2

def add_log_messages(schedule_id, log_messages):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Mevcut log_messages değerini al
        cur.execute("SELECT log_messages FROM schedules WHERE id = %s", (schedule_id,))
        result = cur.fetchone()

        if result and result[0] is not None:
            existing_logs = result[0] 
        else:
            existing_logs = []  # NULL yerine boş liste kullan

        # Yeni mesajları ekle
        updated_logs = existing_logs + log_messages

        # Eğer liste boşsa, NULL yerine '{}' (boş array) ata
        cur.execute(
            """
            UPDATE schedules
            SET log_messages = %s
            WHERE id = %s
            """,
            (updated_logs, schedule_id)
        )

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("add_log_messages fonksiyonunda hata:", e)


def delete_schedule(schedule_id):
    """Belirtilen ID'ye sahip schedule'ı siler."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("DELETE FROM schedules WHERE id = %s", (schedule_id,))
    conn.commit()
    cur.close()
    conn.close()
