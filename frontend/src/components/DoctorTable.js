import React from "react";

const DoctorTable = ({ doctors, seniorities, handleNameChange, handleSeniorityChange, handleSaveChanges }) => {
  return (
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
            <tr key={doctor.id || index}>
              <td>
                <input type="text" className="form-control" value={doctor.name} onChange={(e) => handleNameChange(index, e.target.value)} />
              </td>
              <td>
                <select
                  className="form-select"
                  value={seniorities.find((s) => s.name === doctor.seniority_name)?.id || ""}
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
  );
};

export default DoctorTable;
