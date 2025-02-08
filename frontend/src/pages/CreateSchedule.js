import React, { useState, useEffect } from "react";
import { getAllScheduleData, getScheduleDataById, runAlgorithm } from "../services/apiService";
import ScheduleResultTable from "../components/ScheduleResultTable";
import ScheduleDoctorSummaryTable from "../components/ScheduleDoctorSummaryTable";
import LogMessagesTable from "../components/LogMessagesTable";

const CreateSchedule = () => {
  const [schedules, setSchedules] = useState([]);
  const [selectedScheduleId, setSelectedScheduleId] = useState(null);
  const [scheduleData, setScheduleData] = useState(null);
  const [algorithmResult, setAlgorithmResult] = useState(null);
  const [selectedDoctorCode, setSelectedDoctorCode] = useState(null);
  const [scheduleId, setScheduleId] = useState(null);

  useEffect(() => {
    const fetchSchedules = async () => {
      try {
        const allSchedules = await getAllScheduleData();
        setSchedules(allSchedules);
      } catch (error) {
        console.error("Nöbet listeleri alınırken hata oluştu:", error);
      }
    };
    fetchSchedules();
  }, []);

  useEffect(() => {
    const fetchSelectedSchedule = async () => {
      if (!selectedScheduleId) {
        setScheduleData(null);
        return;
      }
      try {
        const data = await getScheduleDataById(selectedScheduleId);
        setScheduleData(data);
        console.log("Seçili nöbet verisi alındı:", data);
      } catch (error) {
        console.error("Seçili nöbet listesi alınırken hata oluştu:", error);
      }
    };
    fetchSelectedSchedule();
  }, [selectedScheduleId]);

  const handleCreateSchedule = async () => {
    if (!scheduleData) {
      alert("Lütfen bir nöbet listesi seçin!");
      return;
    }

    try {
      const { schedule, schedule_id } = await runAlgorithm(selectedScheduleId);
      console.log("Gerçek schedule ID:", schedule_id);

      setAlgorithmResult(schedule);
      setScheduleId(schedule_id);

      alert("Nöbet listesi başarıyla oluşturuldu!");
    } catch (error) {
      console.error("Hata:", error);
      alert("Nöbet listesi oluşturulamadı!");
    }
  };

  return (
    <div className="container-fluid p-5 background-gradient">
      <h2 className="fw-bold display-5 text-black ms-3 mb-4">Nöbet Listesi Oluştur</h2>

      <div className="row justify-content-center">
        <div className="col-md-4 col-12 mb-3">
          <div className="card bg-dark text-white p-3 rounded-4">
            <h5>Kayıtlı Nöbet Listeleri</h5>
            <select className="form-select mt-2" value={selectedScheduleId || ""} onChange={(e) => setSelectedScheduleId(e.target.value)}>
              <option value="" disabled>
                Seçiniz...
              </option>
              {schedules.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>

            <button className="btn btn-primary mt-3 w-100" onClick={handleCreateSchedule}>
              Nöbet Listesi Oluştur
            </button>
          </div>
        </div>
      </div>

      <ScheduleResultTable schedule={algorithmResult} selectedDoctorCode={selectedDoctorCode} />
      <div className="row">
        <div className="col-md-6">
          <ScheduleDoctorSummaryTable scheduleData={scheduleData} algorithmResult={algorithmResult} setSelectedDoctorCode={setSelectedDoctorCode} />
        </div>

        <div className="col-md-6">
          <LogMessagesTable schedule_id={scheduleId} />
        </div>
      </div>
    </div>
  );
};

export default CreateSchedule;
