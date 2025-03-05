import Footer from "../components/Footer";

export default function HomePage() {
  return (
    <div className="d-flex flex-column background-gradient ">
      <div className="container-fluid p-5 flex-grow-1">
        <div className="d-flex justify-content-center mb-3 pb-4">
          <img src="/henas-bot.png" alt="Henas Bot" width="150" height="150" />
        </div>

        {/* Adımlar Kartları */}
        <div className="row g-4">
          {/* 1. Doktor Bilgileri */}
          <div className="col-md-4 ">
            <div className="card shadow-md bg-dark text-white rounded-4">
              <div className="card-body text-center">
                <h5 className="fw-bold">1️⃣ Doktor Bilgileri</h5>
                <p className="text-white-50">Doktorların kıdem ve isim bilgilerini girin.</p>
                <a href="/hospital" className="btn btn-success w-50">
                  Hastanem'e Git
                </a>
              </div>
            </div>
          </div>

          {/* 2. Nöbet Alanları */}
          <div className="col-md-4">
            <div className="card shadow-sm bg-dark text-white rounded-4">
              <div className="card-body text-center">
                <h5 className="fw-bold">2️⃣ Nöbet Alanları</h5>
                <p className="text-white-50">Kıdemlerin nöbet limitlerini ve alanlarını belirleyin.</p>
                <a href="/hospital#settings" className="btn btn-success w-50 ">
                  Nöbet Ayarlarına Git
                </a>
              </div>
            </div>
          </div>

          {/* 3. Nöbet Listesi Verileri */}
          <div className="col-md-4">
            <div className="card shadow-sm bg-dark text-white rounded-4">
              <div className="card-body text-center">
                <h5 className="fw-bold">3️⃣ Nöbet Listesi Verileri</h5>
                <p className="text-white-50">Doktor kodlarını düzenleyin ve izinleri ekleyin.</p>
                <a href="/schedule-data" className="btn btn-success w-50">
                  Verileri Düzenle
                </a>
              </div>
            </div>
          </div>

          {/* 4. İzin Tanımlama */}
          <div className="col-md-4">
            <div className="card shadow-sm bg-dark text-white rounded-4">
              <div className="card-body text-center">
                <h5 className="fw-bold">4️⃣ Doktor İzinleri</h5>
                <p className="text-white-50">Zorunlu ve opsiyonel izinleri belirleyin.</p>
                <a href="/schedule-data#permissions" className="btn btn-success w-50">
                  İzinleri Ayarla
                </a>
              </div>
            </div>
          </div>

          {/* 5. Nöbet Listesi Oluşturma */}
          <div className="col-md-4">
            <div className="card shadow-sm bg-dark text-white rounded-4">
              <div className="card-body text-center">
                <h5 className="fw-bold">5️⃣ Nöbet Listesi Oluştur</h5>
                <p className="text-white-50">Seçilen nöbet listesi verisiyle liste oluşturun.</p>
                <a href="/create-schedule" className="btn btn-success w-50">
                  Listeyi Oluştur
                </a>
              </div>
            </div>
          </div>

          {/* 6. Kayıtlı Nöbet Listeleri */}
          <div className="col-md-4">
            <div className="card shadow-sm bg-dark text-white rounded-4">
              <div className="card-body text-center">
                <h5 className="fw-bold">6️⃣ Kayıtlı Nöbet Listeleri</h5>
                <p className="text-white-50">Oluşturulan nöbet listelerini görüntüleyin.</p>
                <a href="/schedule-lists" className="btn btn-success w-50">
                  Listelere Git
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
