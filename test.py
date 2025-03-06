import bcrypt
import psycopg2

# PostgreSQL bağlantısı
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="admin",
    host="localhost",  # veya sunucu adresin
    port="5432"
)
cur = conn.cursor()

# Kullanıcı bilgileri
username = "Gazi-Acil"
password = "gazi1234"

# Şifreyi hashle
hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Kullanıcıyı veritabanına ekle
cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))

# Değişiklikleri kaydet
conn.commit()

# Bağlantıyı kapat
cur.close()
conn.close()

print("Yeni kullanıcı eklendi.")
