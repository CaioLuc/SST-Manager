import { useEffect, useState } from "react";
import api from "../services/api";

export default function Dashboard() {
  const [resumo, setResumo] = useState(null);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    api
      .get("/dashboard/resumo")
      .then((res) => setResumo(res.data))
      .catch(() => setErro("Não foi possível carregar os dados do dashboard."));
  }, []);

  return (
    <div>
      <h2>Dashboard de SST</h2>
      {erro && <p style={{ color: "crimson" }}>{erro}</p>}
      {resumo && (
        <div className="card-grid">
          <div className="card">
            <div>Funcionários ativos</div>
            <div className="value">{resumo.total_funcionarios_ativos}</div>
          </div>
          <div className="card">
            <div>ASOs vencendo (30 dias)</div>
            <div className="value">{resumo.asos_vencendo_30_dias}</div>
          </div>
          <div className="card">
            <div>CATs registradas no ano</div>
            <div className="value">{resumo.cats_registradas_ano}</div>
          </div>
          <div className="card">
            <div>NRs vencidas</div>
            <div className="value">{resumo.nrs_vencidas}</div>
          </div>
        </div>
      )}
    </div>
  );
}
