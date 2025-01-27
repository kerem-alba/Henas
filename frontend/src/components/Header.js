import React from "react";

const Header = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <a className="navbar-brand" href="#Anasayfa">
          Nöbet Asistanı
        </a>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <a className="nav-link" href="#nobet-listeleri">
                Nöbet Listeleri
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/hospital">
                Hastanem
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#ayarlar">
                Ayarlar
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#profil">
                Profil
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Header;
