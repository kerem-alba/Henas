import React, { useState, useEffect } from "react";
import { getDoctors, getSeniorities, updateDoctors, getDetailedSeniorities, getShiftAreas, updatedSeniorities } from "../services/apiService";

const Hospital = () => {
  const [doctors, setDoctors] = useState([]);
  const [seniorities, setSeniorities] = useState([]);
  const [detailedSeniorities, setDetailedSeniorities] = useState([]);
  const [shiftAreas, setShiftAreas] = useState([]);

  useEffect(() => {
    const fetchDoctors = async () => {
      try {
        const doctorsData = await getDoctors();
        const sortedDoctors = doctorsData.sort((a, b) => a.name.localeCompare(b.name));
        const senioritiesData = await getSeniorities();
        const seniorityNames = senioritiesData.map((seniority) => ({
          id: seniority.id,
          name: seniority.seniority_name,
        }));
        setDoctors(sortedDoctors);
        setSeniorities(seniorityNames);
      } catch (error) {
        console.error("Hata:", error);
      }
    };
    fetchDoctors();
  }, []);

  useEffect(() => {
    const fetchDetailedSeniorities = async () => {
      try {
        const detailedSenioritiesData = await getDetailedSeniorities();
        setDetailedSeniorities(detailedSenioritiesData);
      } catch (error) {
        console.error("Hata:", error);
      }
    };
    fetchDetailedSeniorities();
  }, []);

  useEffect(() => {
    const fetchShiftAreas = async () => {
      try {
        const shiftAreas = await getShiftAreas();
        setShiftAreas(shiftAreas);
      } catch (error) {
        console.error("Hata:", error);
      }
    };
    fetchShiftAreas();
  }, []);

  const handleSeniorityChange = (index, newSeniorityId) => {
    setDoctors((prevDoctors) => {
      const updatedDoctors = [...prevDoctors];
      updatedDoctors[index].seniority_name = seniorities.find((seniority) => seniority.id === parseInt(newSeniorityId)).name;
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
        id: doctor.id, // Doktorun veritabanındaki benzersiz ID'si
        name: doctor.name.trim(), // Kullanıcının güncellediği isim
        seniority_id: seniorities.find((seniority) => seniority.name === doctor.seniority_name).id, // Seçilen kıdemin ID'si
      }));

      const response = await updateDoctors(payload);
      alert(response.message);
    } catch (error) {
      console.error("Hata:", error);
      alert("Değişiklikler kaydedilirken bir hata oluştu.");
    }
  };

  const handleSeniorityShiftArea = (index, area_name, isChecked) => {
    setDetailedSeniorities((prevSeniorities) => {
      const updatedSeniorities = [...prevSeniorities];
      if (isChecked) {
        // Tik ekleniyorsa
        updatedSeniorities[index].shift_area_names.push(area_name);
      } else {
        // Tik kaldırılıyorsa
        updatedSeniorities[index].shift_area_names = updatedSeniorities[index].shift_area_names.filter((name) => name !== area_name);
      }
      return updatedSeniorities;
    });
  };

  const handleMaxShiftsChange = (index, newMaxShifts) => {
    setDetailedSeniorities((prevSeniorities) => {
      const updatedSeniorities = [...prevSeniorities];
      updatedSeniorities[index].max_shifts_per_month = newMaxShifts;
      return updatedSeniorities;
    });
  };

  const handleSeniorityNameChange = (index, newName) => {
    setDetailedSeniorities((prevSeniorities) => {
      const updatedSeniorities = [...prevSeniorities];
      updatedSeniorities[index].seniority_name = newName;
      return updatedSeniorities;
    });
  };

  const handleSaveSeniorityChanges = async () => {
    try {
      // `shift_area_names`'i `shift_area_ids`'e dönüştür ve tekrarlayanları kaldır
      const cleanedData = detailedSeniorities.map((seniority) => ({
        id: seniority.id,
        name: seniority.seniority_name,
        max_shifts_per_month: seniority.max_shifts_per_month,
        shift_area_ids: [
          ...new Set(
            seniority.shift_area_names
              .map((areaName) => {
                const area = shiftAreas.find((area) => area.area_name === areaName);
                return area ? area.id : null; // `id`'yi bul, yoksa `null` döndür
              })
              .filter((id) => id !== null) // `null` değerleri çıkar
          ),
        ], // Tekil hale getir
      }));

      console.log("Backend'e gönderilen temizlenmiş veri:", cleanedData);

      // Backend'e gönder
      const response = await updatedSeniorities(cleanedData);
      alert(response.message);
    } catch (error) {
      console.error("Kıdem değişikliklerini kaydederken hata oluştu:", error);
      alert("Değişiklikler kaydedilirken bir hata oluştu.");
    }
  };

  return (
    <div className="container mt-4">
      <h2>Veritabanı Yönetimi</h2>
      <div className="row">
        {/* Doktorlar Tablosu */}
        <div className="col-lg-6 col-md-12 mb-4">
          <h3>Doktorlar Listesi</h3>
          <table className="table table-bordered">
            <thead className="thead-dark">
              <tr>
                <th>Ad</th>
                <th>Kıdem</th>
              </tr>
            </thead>
            <tbody>
              {doctors.map((doctor, index) => (
                <tr key={index}>
                  <td>
                    <input type="text" className="form-control" value={doctor.name} onChange={(e) => handleNameChange(index, e.target.value)} />
                  </td>
                  <td>
                    <select
                      className="form-select"
                      value={seniorities.find((seniority) => seniority.name === doctor.seniority_name)?.id || ""}
                      onChange={(e) => handleSeniorityChange(index, e.target.value)}
                    >
                      <option disabled value="">
                        Kıdem Seç
                      </option>
                      {seniorities.map((seniority) => (
                        <option key={seniority.id} value={seniority.id}>
                          {seniority.name}
                        </option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <button className="btn btn-primary mt-3" onClick={handleSaveChanges} disabled={doctors.length === 0}>
            Değişiklikleri Kaydet
          </button>
        </div>

        {/* Kıdem Tablosu */}
        <div className="col-lg-6 col-md-12">
          <h3>Kıdem Listesi</h3>
          <table className="table table-bordered">
            <thead className="thead-dark">
              <tr>
                <th>Kıdem Adı</th>
                <th>Max Nöbet</th>
                <th>Nöbet Alanları</th>
              </tr>
            </thead>
            <tbody>
              {detailedSeniorities.map((seniority, index) => (
                <tr key={seniority.id}>
                  {/* Kıdem Adı */}
                  <td>
                    <input
                      type="text"
                      className="form-control"
                      value={seniority.seniority_name}
                      onChange={(e) => handleSeniorityNameChange(index, e.target.value)}
                    />
                  </td>

                  {/* Max Nöbet */}
                  <td>
                    <input
                      type="number"
                      className="form-control"
                      value={seniority.max_shifts_per_month}
                      onChange={(e) => handleMaxShiftsChange(index, e.target.value)}
                    />
                  </td>

                  {/* Nöbet Alanları */}
                  <td>
                    {shiftAreas.map((area, areaIndex) => (
                      <label key={areaIndex} style={{ display: "block" }}>
                        <input
                          type="checkbox"
                          value={area.area_name}
                          checked={seniority.shift_area_names.includes(area.area_name)}
                          onChange={(e) => handleSeniorityShiftArea(index, area.area_name, e.target.checked)}
                        />{" "}
                        {area.area_name}
                      </label>
                    ))}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <button className="btn btn-primary mt-3" onClick={handleSaveSeniorityChanges} disabled={detailedSeniorities.length === 0}>
            Değişiklikleri Kaydet
          </button>
        </div>
      </div>
    </div>
  );
};

export default Hospital;
