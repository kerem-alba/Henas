import React, { useState } from "react";
import "./styles.css";

const LeavesTable = ({ doctorId, setMandatoryLeaves, setOptionalLeaves }) => {
  const days = Array.from({ length: 30 }, (_, i) => i + 1);
  const shifts = ["Gündüz", "Gece"];

  const [selectedShifts, setSelectedShifts] = useState({});

  const toggleShift = (day, shiftType) => {
    setSelectedShifts((prev) => {
      const current = prev[day]?.[shiftType];
      const shiftIndex = shifts.indexOf(shiftType);

      let newMandatory = [];
      let newOptional = [];

      setMandatoryLeaves((prevMandatory) => {
        newMandatory = prevMandatory.filter((item) => !(item[0] === doctorId && item[1] === day && item[2] === shiftIndex));
        return newMandatory;
      });

      setOptionalLeaves((prevOptional) => {
        newOptional = prevOptional.filter((item) => !(item[0] === doctorId && item[1] === day && item[2] === shiftIndex));
        return newOptional;
      });

      if (current === "mandatory") {
        setOptionalLeaves((prevOptional) => [...prevOptional, [doctorId, day, shiftIndex]]);
        return {
          ...prev,
          [day]: { ...prev[day], [shiftType]: "optional" },
        };
      } else if (current === "optional") {
        return {
          ...prev,
          [day]: { ...prev[day], [shiftType]: undefined },
        };
      } else {
        setMandatoryLeaves((prevMandatory) => [...prevMandatory, [doctorId, day, shiftIndex]]);
        return {
          ...prev,
          [day]: { ...prev[day], [shiftType]: "mandatory" },
        };
      }
    });
  };

  return (
    <div className="table-container">
      <div className="info-box">
        <span>
          <span className="info-square mandatory"></span> Zorunlu İzin
        </span>
        <span>
          <span className="info-square optional"></span> Opsiyonel İzin
        </span>
      </div>

      <table className="mini-table text-dark">
        <thead>
          <tr>
            <th></th>
            {days.map((day) => (
              <th key={day}>{day}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {shifts.map((shiftType) => (
            <tr key={shiftType}>
              <td>{shiftType}</td>
              {days.map((day) => {
                const shiftStatus = selectedShifts[day]?.[shiftType];
                return (
                  <td
                    key={`${doctorId}-${day}-${shiftType}`}
                    onClick={() => toggleShift(day, shiftType)}
                    className={shiftStatus === "mandatory" ? "mandatory" : shiftStatus === "optional" ? "optional" : ""}
                  ></td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default LeavesTable;
