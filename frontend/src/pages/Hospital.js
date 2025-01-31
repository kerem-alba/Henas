import React, { useState, useEffect } from "react";
import { getDoctors, getSeniorities, updateDoctors, getDetailedSeniorities, getShiftAreas, updatedSeniorities } from "../services/apiService";
import DoctorTable from "../components/DoctorTable";
import SeniorityTable from "../components/SeniorityTable";

const Hospital = () => {
  const [doctors, setDoctors] = useState([]);
  const [seniorities, setSeniorities] = useState([]);
  const [detailedSeniorities, setDetailedSeniorities] = useState([]);
  const [shiftAreas, setShiftAreas] = useState([]);

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        const [doctorsData, senioritiesData, detailedSenioritiesData, shiftAreasData] = await Promise.all([
          getDoctors(),
          getSeniorities(),
          getDetailedSeniorities(),
          getShiftAreas(),
        ]);

        const sortedDoctors = doctorsData.sort((a, b) => a.name.localeCompare(b.name));

        const seniorityNames = senioritiesData.map((seniority) => ({
          id: seniority.id,
          name: seniority.seniority_name,
        }));

        setDoctors(sortedDoctors);
        setSeniorities(seniorityNames);
        setDetailedSeniorities(detailedSenioritiesData);
        setShiftAreas(shiftAreasData);
      } catch (error) {
        console.error("Tüm veriler çekilirken hata oluştu:", error);
      }
    };

    fetchAllData();
  }, []);

  const handleSeniorityChange = (index, newSeniorityId) => {
    setDoctors((prevDoctors) => {
      const updatedDoctors = [...prevDoctors];
      const matchedSeniority = seniorities.find((seniority) => seniority.id === parseInt(newSeniorityId));
      if (matchedSeniority) {
        updatedDoctors[index].seniority_name = matchedSeniority.name;
      }
      return updatedDoctors;
    });
  };

  const handleNameChange = (index, newName) => {
    setDoctors((prevDoctors) => {
      const updatedDoctors = [...prevDoctors];
      updatedDoctors[index].name = newName;
      return updatedDoctors;
    });
  };

  const handleSaveChanges = async () => {
    try {
      const payload = doctors.map((doctor) => ({
        id: doctor.id,
        name: doctor.name.trim(),
        seniority_id: seniorities.find((seniority) => seniority.name === doctor.seniority_name).id,
      }));

      const response = await updateDoctors(payload);
      alert(response.message);
    } catch (error) {
      console.error("Doktor değişiklikleri kaydedilirken hata:", error);
      alert("Değişiklikler kaydedilirken bir hata oluştu.");
    }
  };

  const handleSeniorityShiftArea = (index, area_name, isChecked) => {
    setDetailedSeniorities((prevSeniorities) => {
      const updatedSeniorities = [...prevSeniorities];
      if (isChecked) {
        updatedSeniorities[index].shift_area_names.push(area_name);
      } else {
        updatedSeniorities[index].shift_area_names = updatedSeniorities[index].shift_area_names.filter((name) => name !== area_name);
      }
      return updatedSeniorities;
    });
  };

  // Kıdemler: Max Nöbet sayısı değiştirme
  const handleMaxShiftsChange = (index, newMaxShifts) => {
    setDetailedSeniorities((prevSeniorities) => {
      const updatedSeniorities = [...prevSeniorities];
      updatedSeniorities[index].max_shifts_per_month = newMaxShifts;
      return updatedSeniorities;
    });
  };

  // Kıdemler: Kıdem adı değiştirme
  const handleSeniorityNameChange = (index, newName) => {
    setDetailedSeniorities((prevSeniorities) => {
      const updatedSeniorities = [...prevSeniorities];
      updatedSeniorities[index].seniority_name = newName;
      return updatedSeniorities;
    });
  };

  // Kıdemler: Kaydet
  const handleSaveSeniorityChanges = async () => {
    try {
      // shift_area_names => shift_area_ids dönüştür
      const cleanedData = detailedSeniorities.map((seniority) => ({
        id: seniority.id,
        seniority_name: seniority.seniority_name,
        max_shifts_per_month: seniority.max_shifts_per_month,
        shift_area_ids: [
          ...new Set(
            seniority.shift_area_names
              .map((areaName) => {
                const area = shiftAreas.find((a) => a.area_name === areaName);
                return area ? area.id : null;
              })
              .filter((id) => id !== null)
          ),
        ],
      }));

      console.log("Backend'e gönderilen temizlenmiş veri:", cleanedData);

      const response = await updatedSeniorities(cleanedData);
      alert(response.message);
    } catch (error) {
      console.error("Kıdem değişiklikleri kaydedilirken hata:", error);
      alert("Değişiklikler kaydedilirken bir hata oluştu.");
    }
  };

  return (
    <div className="container mt-4">
      <h2>Veritabanı Yönetimi</h2>
      <div className="row">
        {/* Doktor Tablosu */}
        <DoctorTable
          doctors={doctors}
          seniorities={seniorities}
          handleNameChange={handleNameChange}
          handleSeniorityChange={handleSeniorityChange}
          handleSaveChanges={handleSaveChanges}
        />

        {/* Kıdem Tablosu */}
        <SeniorityTable
          detailedSeniorities={detailedSeniorities}
          shiftAreas={shiftAreas}
          handleSeniorityShiftArea={handleSeniorityShiftArea}
          handleMaxShiftsChange={handleMaxShiftsChange}
          handleSeniorityNameChange={handleSeniorityNameChange}
          handleSaveSeniorityChanges={handleSaveSeniorityChanges}
        />
      </div>
    </div>
  );
};

export default Hospital;
