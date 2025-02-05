import React, { useState } from "react";

const ShiftAreasTable = ({
  shiftAreas,
  handleShiftAreaNameChange,
  handleMinDoctorsPerAreaChange,
  handleSaveShiftAreaChanges,
  handleAddShiftArea,
  handleDeleteShiftArea,
}) => {
  const [newAreaName, setNewAreaName] = useState("");

  return (
    <div className="mt-5 w-50">
      <h3>Nöbet Alanları</h3>
      <table className="table table-bordered">
        <thead className="thead-dark">
          <tr>
            <th>#</th>
            <th>Nöbet Alanı</th>
            <th>Min. Nöbetçi</th>
            <th>İşlemler</th>
          </tr>
        </thead>
        <tbody>
          {shiftAreas.map((area, index) => (
            <tr key={area.id || index}>
              <td>{index + 1}</td>
              <td className="d-flex align-items-center">
                <input
                  type="text"
                  className="form-control me-2"
                  value={area.area_name}
                  onChange={(e) => handleShiftAreaNameChange(index, e.target.value)}
                />
              </td>
              <td>
                <input
                  type="number"
                  className="form-control"
                  value={area.min_doctors_per_area}
                  onChange={(e) => handleMinDoctorsPerAreaChange(index, e.target.value)}
                />
              </td>
              <td>
                <button className="btn btn-danger btn-sm ms-auto" onClick={() => handleDeleteShiftArea(area.id)} disabled={!area.id}>
                  <i className="bi bi-trash"></i>
                </button>
              </td>
            </tr>
          ))}
          <tr>
            <td>+</td>
            <td className="d-flex align-items-center">
              <input
                type="text"
                className="form-control me-2"
                value={newAreaName}
                onChange={(e) => setNewAreaName(e.target.value)}
                placeholder="Yeni nöbet alanı adı"
              />
              <button
                className="btn btn-success btn-sm ms-auto"
                type="button"
                style={{ cursor: "pointer" }} // Butona cursor: pointer ekliyoruz
                onClick={() => {
                  if (newAreaName.trim() !== "") {
                    handleAddShiftArea(newAreaName);
                    setNewAreaName("");
                  }
                }}
                disabled={newAreaName.trim() === ""}
              >
                <i className="bi bi-plus-lg"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <button className="btn btn-primary mt-3" onClick={handleSaveShiftAreaChanges} disabled={shiftAreas.length === 0}>
        Değişiklikleri Kaydet
      </button>
    </div>
  );
};

export default ShiftAreasTable;
