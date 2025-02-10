import React, { useEffect, useState } from "react";
import { getScheduleById } from "../services/apiService";

const LogMessagesTable = ({ schedule_id }) => {
  const [logMessages, setLogMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLogs = async () => {
      setLoading(true);
      const schedule = await getScheduleById(schedule_id);
      const logs = schedule.log_messages;
      if (logs.length === 0) {
        setError("Bu schedule için log bulunamadı.");
      } else {
        setLogMessages(logs);
        setError(null);
      }
      setLoading(false);
    };

    if (schedule_id) {
      fetchLogs();
    }
  }, [schedule_id]);

  if (loading) return <> </>;
  if (error) return <p>Hata: {error}</p>;

  return (
    <div className="mt-4">
      <h4 className="text-center bg-dark text-white p-2 rounded-3">Log</h4>
      <div className="card shadow-sm bg-dark">
        <ul className="list-group">
          {logMessages.map((msg, index) => (
            <li key={index} className="list-group-item bg-dark text-light border-secondary">
              {msg}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default LogMessagesTable;
