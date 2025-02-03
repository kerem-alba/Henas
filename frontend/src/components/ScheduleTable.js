import React, { useState } from "react";
import LeavesTable from "./LeavesTable";

const ScheduleTable = ({ doctors, detailedSeniorities, monthYear }) => {
  const [localShiftCounts, setLocalShiftCounts] = useState({});
  const [mandatoryLeaves, setMandatoryLeaves] = useState([]);
  const [optionalLeaves, setOptionalLeaves] = useState([]);

  console.log("mandatoryLeaves!!!!:", mandatoryLeaves);
  console.log("optionalLeaves!!!!!:", optionalLeaves);

  return (
    <div className="table-responsive">
      <table className="table table-bordered">
        <thead>
          <tr>
            <th className="col-1">#</th>
            <th className="col-2">Doktor Adı</th>
            <th className="col-1">Kıdem</th>
            <th className="col-1">Nöbet Alanları</th>
            <th className="col-1">Nöbet Sayısı</th>
            <th className="col-5">İzinler</th>
          </tr>
        </thead>
        <tbody>
          {doctors.map((doctor, index) => {
            const matchedSeniority = detailedSeniorities.find((s) => s.seniority_name === doctor.seniority_name);
            const shiftAreas = matchedSeniority?.shift_area_names.join(", ") || "Alan Yok";

            return (
              <tr key={doctor.id}>
                <td>{index + 1}</td>
                <td>{doctor.name}</td>
                <td>{doctor.seniority_name}</td>
                <td>{shiftAreas}</td>
                <td>
                  <input
                    type="number"
                    className="form-control"
                    value={localShiftCounts[index] || matchedSeniority?.max_shifts_per_month || ""}
                    onChange={(e) => {
                      const newValue = e.target.value;
                      setLocalShiftCounts((prev) => ({ ...prev, [index]: newValue }));
                    }}
                  />
                </td>
                <td>
                  <div style={{ overflowX: "auto", maxWidth: "500px" }}>
                    <LeavesTable setMandatoryLeaves={setMandatoryLeaves} setOptionalLeaves={setOptionalLeaves} />
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default ScheduleTable;
