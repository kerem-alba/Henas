import React from "react";

const SeniorityTable = ({
  detailedSeniorities,
  shiftAreas,
  handleSeniorityShiftArea,
  handleMaxShiftsChange,
  handleSeniorityNameChange,
  handleSaveSeniorityChanges,
}) => {
  return (
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
  );
};

export default SeniorityTable;
