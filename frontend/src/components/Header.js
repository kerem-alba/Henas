/* eslint-disable jsx-a11y/anchor-is-valid */
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
            <div className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" id="nobetListeleriDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Nöbet Listeleri
              </a>
              <div class="dropdown-menu" aria-labelledby="nobetListeleriDropdown">
                <a class="dropdown-item" href="/schedule-data">
                  Nöbet Listesi Verileri
                </a>
                <a class="dropdown-item" href="/create-schedule">
                  Nöbet Listesi Oluştur
                </a>
                <a class="dropdown-item" href="/schedule-lists">
                  Kayıtlı Nöbet Listeleri
                </a>
              </div>
            </div>
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
