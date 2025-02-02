import React, { useState } from "react";

const DoctorTable = ({ doctors, seniorities, handleNameChange, handleSeniorityChange, handleSaveChanges, handleAddDoctor, handleDeleteDoctor }) => {
  const [newDoctorName, setNewDoctorName] = useState("");
  const [newDoctorSeniority, setNewDoctorSeniority] = useState("");

  return (
    <div className="mb-4">
      <h3>Doktorlar Listesi</h3>
      <table className="table table-bordered">
        <thead className="thead-dark">
          <tr>
            <th>#</th>
            <th>Ad</th>
            <th>Kıdem</th>
            <th>İşlem</th> {/* Sil butonu için yeni sütun */}
          </tr>
        </thead>
        <tbody>
          {doctors.map((doctor, index) => (
            <tr key={doctor.id || index}>
              <td>{index + 1}</td>
              <td>
                <input type="text" className="form-control" value={doctor.name} onChange={(e) => handleNameChange(index, e.target.value)} />
              </td>
              <td>
                <select
                  className="form-select"
                  // value={seniorities.find((s) => s.name === doctor.seniority_name)?.id || ""}
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
              <td>
                <button className="btn btn-danger btn-sm" onClick={() => handleDeleteDoctor(doctor.id)} disabled={!doctor.id}>
                  <i className="bi bi-trash"></i> {/* Çöp kutusu ikonu */}
                </button>
              </td>
            </tr>
          ))}
          {/* Yeni doktor ekleme satırı */}
          <tr>
            <td>+</td>
            <td>
              <input
                type="text"
                className="form-control"
                value={newDoctorName}
                onChange={(e) => setNewDoctorName(e.target.value)}
                placeholder="Yeni doktor adı"
              />
            </td>
            <td>
              <select className="form-select" value={newDoctorSeniority} onChange={(e) => setNewDoctorSeniority(e.target.value)}>
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
            <td>
              <button
                className="btn btn-success btn-sm"
                onClick={() => {
                  if (newDoctorName.trim() !== "" && newDoctorSeniority !== "") {
                    handleAddDoctor(newDoctorName, newDoctorSeniority);
                    setNewDoctorName(""); // Temizle
                    setNewDoctorSeniority("");
                  }
                }}
                disabled={newDoctorName.trim() === "" || newDoctorSeniority === ""}
              >
                <i className="bi bi-plus-lg"></i> {/* Ekle butonu için "+" ikonu */}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <button className="btn btn-primary mt-3" onClick={handleSaveChanges} disabled={doctors.length === 0}>
        Değişiklikleri Kaydet
      </button>
    </div>
  );
};

export default DoctorTable;
