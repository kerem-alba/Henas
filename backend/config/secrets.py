from datetime import timedelta

class Config:
    JWT_SECRET_KEY = "supersecretkey"  # Bunu çevresel değişken (env) olarak almak daha güvenli olur.
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
