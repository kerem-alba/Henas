import "./App.css";
import Header from "./components/Header";
import CreateSchedule from "./pages/CreateSchedule";
import Hospital from "./pages/Hospital";
import ScheduleData from "./pages/ScheduleData";
import ScheduleLists from "./pages/ScheduleLists";
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<div>Anasayfa İçeriği</div>} />
        <Route path="/hospital" element={<Hospital />} />
        <Route path="/schedule-data" element={<ScheduleData />} />
        <Route path="/create-schedule" element={<CreateSchedule />} />
        <Route path="/schedule-lists" element={<ScheduleLists />} />
      </Routes>
    </BrowserRouter>
  );
}
export default App;
