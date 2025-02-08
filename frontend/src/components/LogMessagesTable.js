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

  if (loading) return <p>Yükleniyor...</p>;
  if (error) return <p>Hata: {error}</p>;

  return (
    <div>
      <h3>Log Mesajları</h3>
      <ul>
        {logMessages.map((msg, index) => (
          <li key={index}>{msg}</li>
        ))}
      </ul>
    </div>
  );
};

export default LogMessagesTable;
