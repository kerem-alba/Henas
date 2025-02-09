import React from "react";

const ScheduleResultTable = ({ schedule, selectedDoctorCode }) => {
  if (!schedule || schedule.length === 0) {
    return <p className="text-center mt-4">Henüz algoritma çalıştırılmadı.</p>;
  }

  const daysOfWeek = ["Pzt", "Sal", "Çrş", "Per", "Cum", "Cmt", "Paz"];

  const weeks = [];
  for (let i = 0; i < schedule.length; i += 7) {
    weeks.push(schedule.slice(i, i + 7));
  }

  return (
    <div className="table-responsive mt-4">
      <table className="table table-dark table-bordered shadow-md text-center rounded-3" style={{ minWidth: "800px" }}>
        <thead>
          <tr>
            {daysOfWeek.map((day, index) => (
              <th key={index} className="text-center">
                {day}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {weeks.map((week, weekIndex) => (
            <tr key={weekIndex}>
              {week.map((shift, dayIndex) => (
                <td key={dayIndex}>
                  <strong className="d-flex justify-content-center bg-warning text-dark mb-1">{weekIndex * 7 + dayIndex + 1}. Gün</strong>
                  {shift[0].map((code, index) => (
                    <span key={index} className={code === selectedDoctorCode ? "selected-doctor" : ""}>
                      {code}{" "}
                    </span>
                  ))}
                  <br />
                  {shift[1].map((code, index) => (
                    <span key={index} className={code === selectedDoctorCode ? "selected-doctor" : ""}>
                      {code}{" "}
                    </span>
                  ))}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ScheduleResultTable;
