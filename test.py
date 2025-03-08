import psycopg2
import json

# Kaynak (postgres) veritabanına bağlan
source_conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
source_cur = source_conn.cursor()

# Hedef (gazi_db) veritabanına bağlan
target_conn = psycopg2.connect(
    dbname="gazi_db",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
target_cur = target_conn.cursor()

# Tabloları listele
tables = ["doctors", "schedule_data", "schedules", "seniority", "shift_areas"]

for table in tables:
    source_cur.execute(f"SELECT * FROM {table}")
    rows = source_cur.fetchall()
    columns = [desc[0] for desc in source_cur.description]  # Sütun isimlerini al

    for row in rows:
        row = list(row)  # Tuple'ı list'e çevir

        for i, col_name in enumerate(columns):
            if isinstance(row[i], dict) or isinstance(row[i], list):  
                if col_name == "log_messages":  # ARRAY tipindeki sütun
                    row[i] = "{" + ",".join(f'"{x}"' for x in row[i]) + "}" if row[i] else "{}"
                else:  # JSONB tipi olan sütunlar
                    row[i] = json.dumps(row[i])

        placeholders = ', '.join(['%s'] * len(row))
        column_names = ', '.join(columns)
        insert_query = f"""
            INSERT INTO {table} ({column_names}) 
            VALUES ({placeholders})
            ON CONFLICT (id) DO NOTHING
        """
        target_cur.execute(insert_query, row)

    target_conn.commit()
    print(f"{table} tablosu başarıyla taşındı.")

# Bağlantıları kapat
source_cur.close()
source_conn.close()
target_cur.close()
target_conn.close()
