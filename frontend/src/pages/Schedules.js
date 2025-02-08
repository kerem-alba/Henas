import React, { useState, useEffect } from "react";
import { getDoctors, getDetailedSeniorities } from "../services/apiService";
import { getAllScheduleData, getScheduleDataById, deleteScheduleData } from "../services/apiService";
import ScheduleTable from "../components/ScheduleTable";

const Schedules = () => {
  const [doctors, setDoctors] = useState([]);
  const [detailedSeniorities, setDetailedSeniorities] = useState([]);

  // Kayıtlı schedule listesi
  const [schedules, setSchedules] = useState([]); // [{id, name}, ...]
  const [selectedScheduleId, setSelectedScheduleId] = useState(null);

  // Seçili schedule verisi (ScheduleTable'a aktarılacak)
  const [scheduleData, setScheduleData] = useState(null);

  const [isNewScheduleActive, setIsNewScheduleActive] = useState(false);

  // Doktor ve kıdem verilerini getir
  useEffect(() => {
    const fetchBaseData = async () => {
      try {
        const [doctorsData, detailedSenioritiesData] = await Promise.all([getDoctors(), getDetailedSeniorities()]);
        setDoctors(doctorsData);
        setDetailedSeniorities(detailedSenioritiesData);
      } catch (error) {
        console.error("Tüm veriler çekilirken hata oluştu:", error);
      }
    };
    fetchBaseData();
  }, []);

  // Kayıtlı schedule listesini getir
  useEffect(() => {
    const fetchSchedules = async () => {
      try {
        const allSchedules = await getAllScheduleData(); // [{id, name}, ...]
        setSchedules(allSchedules);
      } catch (error) {
        console.error("Schedule listesi alınırken hata:", error);
      }
    };
    fetchSchedules();
  }, []);

  // Seçili schedule değiştiğinde verisini çek
  useEffect(() => {
    const fetchSelectedSchedule = async () => {
      if (!selectedScheduleId) return;
      try {
        const data = await getScheduleDataById(selectedScheduleId);
        setIsNewScheduleActive(false);
        setScheduleData(data);
      } catch (error) {
        console.error("Seçili schedule verisi alınırken hata:", error);
      }
    };
    fetchSelectedSchedule();
  }, [selectedScheduleId]);

  const handleNewSchedule = () => {
    // Yeni liste için tüm veriyi sıfırla
    setSelectedScheduleId(null);
    setScheduleData(null);
    setIsNewScheduleActive(true);
  };

  const handleDeleteSchedule = async () => {
    if (!selectedScheduleId) {
      alert("Lütfen silmek için bir nöbet listesi seçin!");
      return;
    }

    const confirmDelete = window.confirm("Bu nöbet listesini silmek istediğinize emin misiniz?");
    if (!confirmDelete) return;

    try {
      await deleteScheduleData(selectedScheduleId);
      alert("Nöbet listesi başarıyla silindi!");

      // Güncellenmiş listeyi çek
      const updatedSchedules = await getAllScheduleData();
      setSchedules(updatedSchedules);
      setSelectedScheduleId(null);
      setScheduleData(null);
    } catch (error) {
      console.error("Nöbet listesi silinirken hata oluştu:", error);
      alert("Silme işlemi başarısız oldu!");
    }
  };

  return (
    <div className="container-fluid p-5 background-gradient">
      <h2 className="fw-bold display-5 text-black ms-3 mb-4">Nöbet Listesi Verileri</h2>

      <div className="row justify-content-center">
        <div className="col-lg-3 col-12 mb-3" style={{ maxWidth: "350px" }}>
          <div className="card bg-dark text-white p-3 mb-3 mt-4 rounded-4">
            <h5>Kayıtlı Nöbet Listeleri</h5>
            <select className="form-select mt-2" value={selectedScheduleId || ""} onChange={(e) => setSelectedScheduleId(e.target.value)}>
              <option value="" disabled={true}>
                Seçiniz...
              </option>
              {schedules.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>

            <button className={`btn mt-3 ${isNewScheduleActive ? "btn-success" : "btn-secondary"}`} onClick={handleNewSchedule}>
              Yeni Nöbet Listesi Verisi Ekle
            </button>

            <button
              className="btn btn-danger mt-2 w-100"
              onClick={handleDeleteSchedule}
              disabled={!selectedScheduleId} // Seçili bir liste yoksa buton devre dışı
            >
              Seçili Nöbet Listesini Sil
            </button>
          </div>
        </div>

        <div className="col-lg-9 col-12">
          <ScheduleTable doctors={doctors} detailedSeniorities={detailedSeniorities} scheduleData={scheduleData} setScheduleData={setScheduleData} />
        </div>
      </div>
    </div>
  );
};

export default Schedules;
