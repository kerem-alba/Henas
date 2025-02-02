import React, { useState } from "react";
import DraggableShiftAreaList from "./DraggableShiftAreaList"; // Alt bileşen (aşağıda)

const SeniorityTable = ({
  detailedSeniorities,
  shiftAreas,
  handleSeniorityShiftArea,
  handleMaxShiftsChange,
  handleSeniorityNameChange,
  handleSaveSeniorityChanges,
  handleAddSeniority,
  handleDeleteSeniority,
}) => {
  const [newSeniorityName, setNewSeniorityName] = useState("");
  const [newMaxShifts, setNewMaxShifts] = useState("");

  return (
    <div className="mb-5">
      <h3>Kıdem Listesi</h3>
      <table className="table table-bordered">
        <thead className="thead-dark">
          <tr>
            <th className="col-1">#</th>
            <th className="col-4">Kıdem Adı</th>
            <th className="col-2"> Max Nöbet</th>
            <th className="col-4">Nöbet Alanları</th>
            <th className="col-1">İşlem</th>
          </tr>
        </thead>
        <tbody>
          {detailedSeniorities.map((seniority, index) => (
            <tr key={seniority.id}>
              <td>{index + 1}</td>

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

              <td>
                <DraggableShiftAreaList
                  allShiftAreas={shiftAreas}
                  activeAreaNames={seniority.shift_area_names}
                  onUpdate={(updatedActiveNames) => {
                    seniority.shift_area_names = updatedActiveNames;
                  }}
                />
              </td>

              <td>
                <button className="btn btn-danger btn-sm" onClick={() => handleDeleteSeniority(seniority.id)} disabled={!seniority.id}>
                  <i className="bi bi-trash"></i>
                </button>
              </td>
            </tr>
          ))}

          {/* Yeni kıdem ekleme satırı */}
          <tr>
            <td>+</td>
            <td>
              <input
                type="text"
                className="form-control"
                value={newSeniorityName}
                onChange={(e) => setNewSeniorityName(e.target.value)}
                placeholder="Yeni kıdem adı"
              />
            </td>
            <td>
              <input
                type="number"
                className="form-control"
                value={newMaxShifts}
                onChange={(e) => setNewMaxShifts(e.target.value)}
                placeholder="Max nöbet"
              />
            </td>
            <td>-</td> {/* Yeni eklemede alan listesi yok */}
            <td>
              <button
                className="btn btn-success btn-sm"
                onClick={() => {
                  if (newSeniorityName.trim() !== "" && newMaxShifts !== "") {
                    handleAddSeniority(newSeniorityName, newMaxShifts);
                    setNewSeniorityName("");
                    setNewMaxShifts("");
                  }
                }}
                disabled={newSeniorityName.trim() === "" || newMaxShifts === ""}
              >
                <i className="bi bi-plus-lg"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <button className="btn btn-primary mt-3" onClick={handleSaveSeniorityChanges} disabled={detailedSeniorities.length === 0}>
        Değişiklikleri Kaydet
      </button>
    </div>
  );
};

export default SeniorityTable;
