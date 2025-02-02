import React, { useState, useEffect } from "react";
import { DayPicker } from "react-day-picker";
import "react-day-picker/style.css";
import { format } from "date-fns";
import "./style.css";

const LeaveModal = ({ isOpen, onClose, monthYear, onSave }) => {
  console.log("LeaveModal Render Edildi!");
  console.log("LeaveModal Props - isOpen:", isOpen);

  const [selectedDays, setSelectedDays] = useState({});

  useEffect(() => {
    console.log("LeaveModal isOpen Değişti:", isOpen);
  }, [isOpen]);

  if (!isOpen) return null; // Eğer isOpen false ise hiçbir şey render etme!

  const handleDayClick = (day, shiftType) => {
    const dayKey = format(day, "yyyy-MM-dd");
    setSelectedDays((prev) => ({
      ...prev,
      [dayKey]: prev[dayKey] === shiftType ? null : shiftType, // Eğer aynı shift varsa kaldır
    }));
  };

  const handleSave = () => {
    onSave(selectedDays);
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>{format(new Date(monthYear), "MMMM yyyy")} İzin Takvimi</h3>

        <DayPicker
          mode="multiple"
          selected={Object.keys(selectedDays).map((day) => new Date(day))}
          onDayClick={(day) => handleDayClick(day, "shift1")}
        />

        <div className="modal-actions">
          <button onClick={onClose}>İptal</button>
          <button onClick={handleSave}>Kaydet</button>
        </div>
      </div>
    </div>
  );
};

export default LeaveModal;
