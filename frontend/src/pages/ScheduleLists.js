import { useEffect, useState } from "react";
import { getSchedules, getScheduleById, getScheduleDataById } from "../services/apiService";
import ScheduleResultTable from "../components/ScheduleResultTable";
import ScheduleDoctorSummaryTable from "../components/ScheduleDoctorSummaryTable";
import LogMessagesTable from "../components/LogMessagesTable";

const ScheduleLists = () => {
  const [savedSchedules, setSavedSchedules] = useState([]);
  const [schedule, setSchedule] = useState(null);
  const [fitnessScore, setFitnessScore] = useState(null);
  const [logMessages, setLogMessages] = useState(null);
  const [schedule_id, setSchedule_id] = useState(null);
  const [selectedDoctorCode, setSelectedDoctorCode] = useState(null);
  const [scheduleData, setScheduleData] = useState(null);

  // Schedules listesini çeken useEffect
  useEffect(() => {
    const fetchSchedules = async () => {
      try {
        const data = await getSchedules();
        setSavedSchedules(data);
      } catch (error) {
        console.error("Nöbet listelerini getirirken hata oluştu:", error);
      }
    };
    fetchSchedules();
  }, []);

  // Dropdown seçim işlevi
  const handleSelectSchedule = async (selectedId) => {
    if (!selectedId) return;

    // Seçilen schedule objesini bul
    const selectedSchedule = savedSchedules.find((item) => item.id === parseInt(selectedId));

    if (!selectedSchedule) {
      console.error("Seçilen schedule bulunamadı. ID:", selectedId);
      return;
    }

    // schedule_data_id'yi al
    const { schedule_data_id } = selectedSchedule;
    console.log("Selected schedule_data_id:", schedule_data_id);

    // Seçilen schedule'ın detaylarını getir
    const scheduleResult = await getScheduleById(selectedId);

    // schedule_data_id ile ek veriyi al
    let scheduleDataResponse = null;
    if (schedule_data_id) {
      scheduleDataResponse = await getScheduleDataById(schedule_data_id);
      console.log("scheduleDataResponse:", scheduleDataResponse.data);
    }

    // State güncelle
    setSchedule(scheduleResult.schedule);
    setFitnessScore(scheduleResult.fitness_score);
    setLogMessages(scheduleResult.log_messages);
    setSchedule_id(scheduleResult.id);
    setScheduleData(scheduleDataResponse);
  };

  return (
    <div className="container-fluid p-5 background-gradient full-screen">
      <h2 className="fw-bold display-5 text-black ms-3 mb-4">Nöbet Listeleri</h2>
      <div className="card bg-dark text-white p-3 rounded-4 w-50">
        <h5>Kayıtlı Nöbet Listeleri</h5>
        <select onChange={(e) => handleSelectSchedule(e.target.value)}>
          <option value="" disabled>
            Seçiniz...
          </option>
          {savedSchedules.map((sch) => (
            <option key={sch.id} value={sch.id}>
              {`${sch.schedule_data_name} - ${sch.fitness_score}`}
            </option>
          ))}
        </select>
      </div>

      {/* Seçilen schedule varsa bileşenlere gönder */}
      {schedule && (
        <>
          <ScheduleResultTable schedule={schedule} selectedDoctorCode={selectedDoctorCode} />

          <div className="row">
            <div className="col-md-6">
              <ScheduleDoctorSummaryTable scheduleData={scheduleData} algorithmResult={schedule} setSelectedDoctorCode={setSelectedDoctorCode} />
            </div>

            <div className="col-md-6">
              <LogMessagesTable schedule_id={schedule_id} />
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ScheduleLists;
