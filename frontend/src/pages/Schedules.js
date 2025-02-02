import React, { useState, useEffect } from "react";
import { getDoctors, getDetailedSeniorities } from "../services/apiService";
import ScheduleTable from "../components/ScheduleTable";

const Schedules = () => {
  const [doctors, setDoctors] = useState([]);
  const [detailedSeniorities, setDetailedSeniorities] = useState([]);

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

  const monthYear = "2024-02-01";

  return (
    <div className="container mt-4">
      <h2>Nöbet Programı Oluştur</h2>
      <ScheduleTable doctors={doctors} detailedSeniorities={detailedSeniorities} monthYear={monthYear} />
      <button className="btn btn-primary mt-3" onClick={() => console.log("Algoritmayı çalıştır")}>
        Algoritmayı Çalıştır
      </button>
    </div>
  );
};

export default Schedules;
