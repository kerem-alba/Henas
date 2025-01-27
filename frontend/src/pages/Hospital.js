import React, { useState, useEffect } from "react";
import { getDoctors, getSeniorities, updateDoctors } from "../services/apiService";

const Hospital = () => {
  const [doctors, setDoctors] = useState([]);
  const [seniorities, setSeniorities] = useState([]);

  useEffect(() => {
    const fetchDoctors = async () => {
      try {
        const doctorsData = await getDoctors();
        const senioritiesData = await getSeniorities();

        const seniorityNames = senioritiesData.map((seniority) => ({
          id: seniority.id,
          name: seniority.seniority_name,
        }));
        setDoctors(doctorsData);
        setSeniorities(seniorityNames);
      } catch (error) {
        console.error("Hata:", error);
      }
    };
    fetchDoctors();
  }, []);

  const handleSeniorityChange = (index, newSeniorityId) => {
    setDoctors((prevDoctors) => {
      const updatedDoctors = [...prevDoctors];
      updatedDoctors[index].seniority_name = seniorities.find((level) => level.id === parseInt(newSeniorityId)).name;
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
        name: doctor.name,
        seniority_id: seniorities.find((level) => level.name === doctor.seniority_name).id,
      }));

      const result = await updateDoctors(payload); // Servisi çağır
      alert(result.message); // Backend'den gelen mesajı göster
    } catch (error) {
      alert("Değişiklikler kaydedilirken bir hata oluştu.");
    }
  };

  return (
    <div className="container mt-4">
      <h2>Doktorlar Listesi</h2>
      <table className="table table-bordered">
        <thead>
          <tr>
            <th>Ad</th>
            <th>Kıdem</th>
          </tr>
        </thead>
        <tbody>
          {doctors.map((doctor, index) => (
            <tr key={index}>
              {/* İsim Alanı - Düzenlenebilir */}
              <td>
                <input type="text" className="form-control" value={doctor.name} onChange={(e) => handleNameChange(index, e.target.value)} />
              </td>

              {/* Kıdem Alanı - Dropdown */}
              <td>
                <select
                  className="form-select"
                  value={seniorities.find((level) => level.name === doctor.seniority_name)?.id || ""}
                  onChange={(e) => handleSeniorityChange(index, e.target.value)}
                >
                  <option disabled value="">
                    Kıdem Seç
                  </option>
                  {seniorities.map((level) => (
                    <option key={level.id} value={level.id}>
                      {level.name}
                    </option>
                  ))}
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Değişiklikleri Kaydet Butonu */}
      <button
        className="btn btn-primary mt-3"
        onClick={handleSaveChanges}
        disabled={doctors.length === 0} // Eğer doktor listesi boşsa butonu devre dışı bırak
      >
        Değişiklikleri Kaydet
      </button>
    </div>
  );
};

export default Hospital;
