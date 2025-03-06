import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/apiService";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const data = await login(username, password);
      console.log("Giriş başarılı:", data);

      navigate("/home");
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="background-gradient">
      <div className="container d-flex justify-content-center align-items-center min-vh-100">
        <div className="card p-4 shadow-lg rounded-4" style={{ maxWidth: "400px", width: "100%" }}>
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
