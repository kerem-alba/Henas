import "./App.css";
import Header from "./components/Header";
import Hospital from "./pages/Hospital";
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<div>Anasayfa İçeriği</div>} />
        <Route path="/hospital" element={<Hospital />} />
      </Routes>
    </BrowserRouter>
  );
}
export default App;
