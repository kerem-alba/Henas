import React, { useState, useEffect } from "react";
import LeavesTable from "./LeavesTable";

const ScheduleTable = ({ doctors, detailedSeniorities, setScheduleData }) => {
  const [localShiftCounts, setLocalShiftCounts] = useState({});
  const [mandatoryLeaves, setMandatoryLeaves] = useState([]);
  const [optionalLeaves, setOptionalLeaves] = useState([]);
  const [doctorCodes, setDoctorCodes] = useState({});
  const [expandedRow, setExpandedRow] = useState(null); // Açılan satırı takip eden state

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
  };

  // Satır açma/kapatma fonksiyonu
  const toggleRow = (doctorId) => {
    setExpandedRow(expandedRow === doctorId ? null : doctorId);
  };

  return (
    <div className="mt-4 w-75 mx-auto">
      <h3 className="text-center bg-dark text-white p-3 shadow-md rounded-4">Nöbet Listesi</h3>
      <table className="table table-dark table-striped table-hover shadow-md" style={{ borderRadius: "15px", overflow: "hidden" }}>
        <thead className="thead-dark">
          <tr className="align-middle">
            <th className="col-1 text-center">#</th>
            <th className="col-1">Kod</th>
            <th className="col-2">Doktor Adı</th>
            <th className="col-1">Kıdem</th>
            <th className="col-1">Nöbet Alanları</th>
            <th className="col-1">Nöbet Sayısı</th>
            <th className="col-1 text-center">İzinler</th>
          </tr>
        </thead>
        <tbody>
          {doctors.map((doctor, index) => {
            const matchedSeniority = detailedSeniorities.find((s) => s.seniority_name === doctor.seniority_name);
            const shiftAreas = matchedSeniority?.shift_area_names.join(", ") || "Alan Yok";

            return (
              <React.Fragment key={doctor.id}>
                {/* Ana Satır */}
                <tr className="align-middle">
                  <td className="align-middle text-center">{index + 1}</td>
                  <td>
                    <input
                      type="text"
                      className="form-control bg-secondary text-white"
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
                        const newValue = Number(e.target.value);
                        setLocalShiftCounts((prev) => ({ ...prev, [index]: newValue }));
                      }}
                    />
                  </td>
                  {/* Açılır-Kapanır Butonu */}
                  <td className="text-center">
                    <button className="btn btn-sm btn-outline-light" onClick={() => toggleRow(doctor.id)}>
                      {expandedRow === doctor.id ? "İzinleri Gizle" : "İzinleri Göster"}
                    </button>
                  </td>
                </tr>

                {/* Açılan İzinler Satırı */}
                {expandedRow === doctor.id && (
                  <tr>
                    <td colSpan="7" className="p-0">
                      <div className="bg-light p-3">
                        <LeavesTable doctorId={doctor.id} setMandatoryLeaves={setMandatoryLeaves} setOptionalLeaves={setOptionalLeaves} />
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            );
          })}
        </tbody>
      </table>
      <button className="btn btn-success w-100 shadow-md rounded-3" onClick={handleSaveScheduleData}>
        Kaydet
      </button>
    </div>
  );
};

export default ScheduleTable;
