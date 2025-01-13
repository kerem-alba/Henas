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

    # Doktorları ve nöbet sayılarını çek
    cur.execute("""
        SELECT d.name, s.id AS seniority, s.max_shifts_per_month
        FROM doctors d
        JOIN seniority s ON d.seniority_id = s.id
    """)


    doctors = cur.fetchall()

    cur.close()
    conn.close()

    return doctors
