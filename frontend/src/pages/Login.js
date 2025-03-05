import React, { useState } from "react";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); // Hata mesajını sıfırlayalım

    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        // Eğer login başarılıysa, token'ı localStorage'a kaydedelim
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);

        // Giriş başarılıysa anasayfaya yönlendir
        window.location.href = "/home";
      } else {
        const errorData = await response.json();
        setError(errorData.error || "Geçersiz kullanıcı adı veya şifre");
      }
    } catch (err) {
      setError("Bir hata oluştu.");
    }
  };

  return (
    <div className="background-gradient">
      <div className="container d-flex justify-content-center align-items-center min-vh-100 ">
        <div className="card p-4 shadow-lg rounded-4 " style={{ maxWidth: "400px", width: "100%" }}>
          <h2 className="text-center mb-4">Giriş Yap</h2>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label htmlFor="username" className="form-label">
                Kullanıcı Adı
              </label>
              <input type="text" id="username" className="form-control" value={username} onChange={(e) => setUsername(e.target.value)} required />
            </div>
            <div className="mb-3">
              <label htmlFor="password" className="form-label">
                Şifre
              </label>
              <input type="password" id="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} required />
            </div>
            {error && <div className="alert alert-danger">{error}</div>}
            <button type="submit" className="btn btn-primary w-100">
              Giriş Yap
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
