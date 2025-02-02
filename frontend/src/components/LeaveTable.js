import { useState } from "react";
import LeaveModal from "./LeaveModal";

const LeaveTable = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [mandatoryLeaves, setMandatoryLeaves] = useState([]);

  const handleOpenModal = () => setIsModalOpen(true);
  const handleCloseModal = () => setIsModalOpen(false);

  const handleSaveLeaves = (selectedShifts) => {
    setMandatoryLeaves(selectedShifts);
    setIsModalOpen(false);
  };

  return (
    <div>
      <button onClick={handleOpenModal}>Zorunlu İzin Ekle</button>

      {isModalOpen && <LeaveModal onClose={handleCloseModal} onSave={handleSaveLeaves} />}

      <h4>Seçilen Zorunlu İzinler:</h4>
      <pre>{JSON.stringify(mandatoryLeaves, null, 2)}</pre>
    </div>
  );
};

export default LeaveTable;
