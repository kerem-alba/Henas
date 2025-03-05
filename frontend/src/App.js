import "./App.css";
import Header from "./components/Header";
import CreateSchedule from "./pages/CreateSchedule";
import Hospital from "./pages/Hospital";
import ScheduleData from "./pages/ScheduleData";
import ScheduleLists from "./pages/ScheduleLists";
import Home from "./pages/Home";
import Login from "./pages/Login";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import PrivateRoute from "./components/PrivateRoute"; // PrivateRoute'ı import ettik

function App() {
  // window.location.pathname ile şu anki URL'yi alıyoruz
  const isLoginPage = window.location.pathname === "/login";

  return (
    <BrowserRouter>
      {/* Eğer şu anki sayfa login sayfası değilse Header'ı göster */}
      {!isLoginPage && <Header />}

      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/home" />} />
        <Route path="/home" element={<Home />} />

        {/* Login hariç tüm sayfaları PrivateRoute ile koruyoruz */}
        <Route path="/hospital" element={<PrivateRoute element={<Hospital />} />} />
        <Route path="/schedule-data" element={<PrivateRoute element={<ScheduleData />} />} />
        <Route path="/create-schedule" element={<PrivateRoute element={<CreateSchedule />} />} />
        <Route path="/schedule-lists" element={<PrivateRoute element={<ScheduleLists />} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
