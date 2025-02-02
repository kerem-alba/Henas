import React, { useState } from "react";
import LeaveModal from "../modals/LeaveModal";

const ScheduleTable = ({ doctors, detailedSeniorities, monthYear }) => {
  const [localShiftCounts, setLocalShiftCounts] = useState({});
  const [isLeaveModalOpen, setIsLeaveModalOpen] = useState(false);
  const [selectedDoctorIndex, setSelectedDoctorIndex] = useState(null);
  const [leaveType, setLeaveType] = useState(null);

  // Modal'ı aç
  const openLeaveModal = (doctorIndex, type) => {
    console.log("Modal Açılıyor:", doctorIndex, type); // Kontrol için
    setSelectedDoctorIndex(doctorIndex);
    setLeaveType(type);
    setIsLeaveModalOpen(true);
  };

  // Modal'ı kapat
  const closeLeaveModal = () => {
    console.log("closeLeaveModal çağrıldı!"); // Kapatma işlemi tetikleniyor mu?

    setIsLeaveModalOpen(false);
    setSelectedDoctorIndex(null);
    setLeaveType(null);
  };

  // İzinleri kaydet
  const handleSaveLeaves = (selectedDays) => {
    console.log("Seçilen izinler:", selectedDays);
    console.log("Doktor Index:", selectedDoctorIndex);
    console.log("İzin Türü:", leaveType);
    // Burada izinleri doktorun verisine kaydedebilirsiniz
  };

  console.log("Modal Render Durumu:", isLeaveModalOpen);
  console.log("Final Modal Render Durumu:", isLeaveModalOpen);

  return (
    <div className="table-responsive">
      <table className="table table-bordered">
        <thead>
          <tr>
            <th>#</th>
            <th>Doktor Adı</th>
            <th>Kıdem</th>
            <th>Nöbet Alanları</th>
            <th>Nöbet Sayısı</th>
            <th>Zorunlu İzinler</th>
            <th>Opsiyonel İzinler</th>
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
                  <button className="btn btn-warning" onClick={() => openLeaveModal(index, "mandatory")}>
                    Zorunlu İzin Ekle
                  </button>
                </td>
                <td>
                  <button className="btn btn-info" onClick={() => openLeaveModal(index, "optional")}>
                    Opsiyonel İzin Ekle
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {/* Modal yalnızca açıkken render edilecek */}
      {isLeaveModalOpen && (
        <LeaveModal
          isOpen={isLeaveModalOpen} // ✅ isOpen olarak gönderiyoruz!
          onClose={closeLeaveModal}
          monthYear={monthYear}
          onSave={handleSaveLeaves}
        />
      )}
    </div>
  );
};

export default ScheduleTable;
