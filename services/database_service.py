import psycopg2 

# Veritabanı bağlantı bilgileri
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": 5432
}

def get_doctors():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Doktorların kıdem bilgilerini ve nöbet alanlarını çek
    cur.execute("""
        SELECT d.name, d.seniority_id, s.max_shifts_per_month, array_agg(sa.area_name)
        FROM doctors d
        JOIN seniority s ON d.seniority_id = s.id
        JOIN LATERAL unnest(s.shift_area_ids) AS area_id ON true
        JOIN shift_areas sa ON sa.id = area_id
        GROUP BY d.id, d.name, d.seniority_id, s.max_shifts_per_month
        ORDER BY d.id
    """)
    result = cur.fetchall()

    # Veritabanından gelen veriyi düzenle
    doctors = []
    for row in result:
        name, seniority, shift_count, shift_areas = row
        doctors.append((name, seniority, shift_count, shift_areas))

    cur.close()
    conn.close()
    return doctors

def get_shift_areas():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    cur.execute("SELECT id, area_name FROM shift_areas")
    shift_areas = {row[1]: row[0] for row in cur.fetchall()}
    
    cur.close()
    conn.close()
    
    return shift_areas

def get_doctor_seniority():
    """
    Veritabanından doktor kıdem bilgilerini ve kıdeme uygun nöbet alanlarını alır.
    :return: {'A': {'level': 1, 'areas': [1, 2]}, ...} formatında sözlük döndürür.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Doktor kıdem bilgilerini ve nöbet alanlarını al
    cur.execute("""
        SELECT d.name, s.id, s.shift_area_ids
        FROM doctors d
        JOIN seniority s ON d.seniority_id = s.id
    """)
    result = cur.fetchall()

    cur.close()
    conn.close()

    # Sonuçları düzenle
    doctor_seniority = {}
    for code, level, areas in result:
        doctor_seniority[code] = {"level": level, "areas": areas}

    return doctor_seniority



def get_doctor_mapping():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Doktor kodlarını ve kimliklerini al
    cur.execute("SELECT id, name FROM doctors")
    result = cur.fetchall()

    # Sonuçları sözlük formatında döndür
    doctor_mapping = {row[1][0].upper(): row[0] for row in result}

    cur.close()
    conn.close()

    return doctor_mapping

def get_seniority_levels():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Tüm kıdem seviyelerini al
    cur.execute("SELECT id FROM seniority ORDER BY id")
    result = cur.fetchall()

    cur.close()
    conn.close()

    # Sonuçları bir set olarak döndür
    return {row[0] for row in result}
