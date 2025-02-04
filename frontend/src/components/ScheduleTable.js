import React, { useState, useEffect } from "react";
import LeavesTable from "./LeavesTable";

const ScheduleTable = ({ doctors, detailedSeniorities, setScheduleData }) => {
  const [localShiftCounts, setLocalShiftCounts] = useState({});
  const [mandatoryLeaves, setMandatoryLeaves] = useState([]);
  const [optionalLeaves, setOptionalLeaves] = useState([]);
  const [doctorCodes, setDoctorCodes] = useState({});

  // Doktorlara sırayla A, B, C, ... şeklinde kod atama
  useEffect(() => {
    const assignedCodes = {};
    doctors.forEach((doctor, index) => {
      assignedCodes[doctor.id] = String.fromCharCode(65 + index); // 'A', 'B', 'C', ...
    });
    setDoctorCodes(assignedCodes);
  }, [doctors]);

  const handleSaveScheduleData = () => {
    const newScheduleData = doctors.map((doctor, index) => {
      const matchedSeniority = detailedSeniorities.find((s) => s.seniority_name === doctor.seniority_name);
      const shiftCount = localShiftCounts[index] || matchedSeniority?.max_shifts_per_month || 0;
      const seniority_id = matchedSeniority.id;
      const shift_area_ids = matchedSeniority.shift_area_ids;

      return {
        code: doctorCodes[doctor.id], // Kodu dahil ettik
        name: doctor.name,
        seniority_id: seniority_id,
        shift_count: shiftCount,
        shift_areas: shift_area_ids,
        mandatory_leaves: mandatoryLeaves.filter((leave) => leave[0] === doctor.id).map((leave) => [leave[1], leave[2]]),
        optional_leaves: optionalLeaves.filter((leave) => leave[0] === doctor.id).map((leave) => [leave[1], leave[2]]),
      };
    });

    setScheduleData(newScheduleData);
    console.log("Kaydedilen veri:", newScheduleData);
    console.log("Mandatory izinler:", mandatoryLeaves);
    console.log("Optional izinler:", optionalLeaves);
  };

  return (
    <div className="table-responsive">
      <table className="table table-bordered">
        <thead>
          <tr>
            <th className="col-1">#</th>
            <th className="col-2">Kod</th>
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
                <td>
                  <input
                    type="text"
                    className="form-control"
                    value={doctorCodes[doctor.id] || ""}
                    onChange={(e) => {
                      setDoctorCodes((prev) => ({
                        ...prev,
                        [doctor.id]: e.target.value.toUpperCase(),
                      }));
                    }}
                  />
                </td>
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
                    <LeavesTable doctorId={doctor.id} setMandatoryLeaves={setMandatoryLeaves} setOptionalLeaves={setOptionalLeaves} />
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <button className="btn btn-primary" onClick={handleSaveScheduleData}>
        Kaydet
      </button>
    </div>
  );
};

export default ScheduleTable;
