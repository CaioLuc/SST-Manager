import { Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Funcionarios from "./pages/Funcionarios";
import EPIs from "./pages/EPIs";
import ASOs from "./pages/ASOs";
import NRs from "./pages/NRs";
import CATs from "./pages/CATs";

export default function App() {
  return (
    <div className="layout">
      <Sidebar />
      <main className="content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/funcionarios" element={<Funcionarios />} />
          <Route path="/epis" element={<EPIs />} />
          <Route path="/asos" element={<ASOs />} />
          <Route path="/nrs" element={<NRs />} />
          <Route path="/cats" element={<CATs />} />
        </Routes>
      </main>
    </div>
  );
}
