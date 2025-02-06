import React, { useState, useEffect } from "react";
import { getDoctors, getDetailedSeniorities, runAlgorithm } from "../services/apiService";
import ScheduleTable from "../components/ScheduleTable";

const Schedules = () => {
  const [doctors, setDoctors] = useState([]);
  const [detailedSeniorities, setDetailedSeniorities] = useState([]);
  const [scheduleData, setScheduleData] = useState([]);

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        const [doctorsData, detailedSenioritiesData] = await Promise.all([getDoctors(), getDetailedSeniorities()]);
        setDoctors(doctorsData);
        setDetailedSeniorities(detailedSenioritiesData);
      } catch (error) {
        console.error("Tüm veriler çekilirken hata oluştu:", error);
      }
    };
    fetchAllData();
  }, []);

  return (
    <div className="container-fluid p-5 background-gradient">
      <h2 className="fw-bold display-5 text-black ms-3">Hastane Veritabanı</h2>
      <ScheduleTable doctors={doctors} detailedSeniorities={detailedSeniorities} setScheduleData={setScheduleData} />
      <button className="btn btn-primary mt-3" onClick={() => runAlgorithm(scheduleData)}>
        Algoritmayı Çalıştır
      </button>
    </div>
  );
};

export default Schedules;
