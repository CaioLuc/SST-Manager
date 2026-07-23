import { useEffect, useState } from "react";
import api from "../services/api";

export default function Funcionarios() {
  const [funcionarios, setFuncionarios] = useState([]);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    api
      .get("/funcionarios/")
      .then((res) => setFuncionarios(res.data))
      .catch(() => setErro("Não foi possível carregar os funcionários."));
  }, []);

  return (
    <div>
      <h2>Funcionários</h2>
      {erro && <p style={{ color: "crimson" }}>{erro}</p>}
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>CPF</th>
            <th>Cargo</th>
            <th>Setor</th>
            <th>Admissão</th>
            <th>Ativo</th>
          </tr>
        </thead>
        <tbody>
          {funcionarios.map((f) => (
            <tr key={f.id}>
              <td>{f.nome}</td>
              <td>{f.cpf}</td>
              <td>{f.cargo}</td>
              <td>{f.setor}</td>
              <td>{f.data_admissao}</td>
              <td>{f.ativo ? "Sim" : "Não"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
