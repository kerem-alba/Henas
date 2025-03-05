import requests

BASE_URL = "http://127.0.0.1:5000"

# 1. Login olup access token ve refresh token alalım
login_data = {"username": "testuser", "password": "testpass"}
login_response = requests.post(f"{BASE_URL}/login", json=login_data)

if login_response.status_code == 200:
    data = login_response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    print("Giriş başarılı, alınan access token:", access_token)
    print("Alınan refresh token:", refresh_token)

    # 2. Alınan refresh token ile /refresh endpoint'ine istek atalım
    headers = {"Authorization": f"Bearer {refresh_token}"}
    refresh_response = requests.post(f"{BASE_URL}/refresh", headers=headers)

    if refresh_response.status_code == 200:
        new_access_token = refresh_response.json().get("access_token")
        print("Yeni alınan access token:", new_access_token)
    else:
        print("Refresh token ile yeni access token alınamadı.", refresh_response.json())
else:
    print("Login başarısız:", login_response.json())
