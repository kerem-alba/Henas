import React, { useState, useEffect } from "react";
import { getDoctors, getDetailedSeniorities, getSeniorities, runAlgorithm } from "../services/apiService";
import ScheduleTable from "../components/ScheduleTable";

const Schedules = () => {
  const [doctors, setDoctors] = useState([]);
  const [detailedSeniorities, setDetailedSeniorities] = useState([]);
  const [seniorities, setSeniorities] = useState([]);
  const [scheduleData, setScheduleData] = useState([]);

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        const [doctorsData, detailedSenioritiesData, seniorities] = await Promise.all([getDoctors(), getDetailedSeniorities(), getSeniorities()]);
        setDoctors(doctorsData);
        setDetailedSeniorities(detailedSenioritiesData);
        setSeniorities(seniorities);
      } catch (error) {
        console.error("Tüm veriler çekilirken hata oluştu:", error);
      }
    };
    fetchAllData();
  }, []);

  console.log("Doctors:", doctors);
  console.log("Detailed Seniorities:", detailedSeniorities);
  console.log("Seniorities:", seniorities);

  return (
    <div className="container mt-4">
      <h2>Nöbet Programı Oluştur</h2>
      <ScheduleTable doctors={doctors} detailedSeniorities={detailedSeniorities} setScheduleData={setScheduleData} />
      <button className="btn btn-primary mt-3" onClick={() => runAlgorithm(scheduleData)}>
        Algoritmayı Çalıştır
      </button>
    </div>
  );
};

export default Schedules;
