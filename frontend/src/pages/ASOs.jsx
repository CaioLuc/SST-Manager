import { useEffect, useState } from "react";
import api from "../services/api";

export default function ASOs() {
  const [dados, setDados] = useState([]);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    api
      .get("/asos/")
      .then((res) => setDados(res.data))
      .catch(() => setErro("Não foi possível carregar os dados de ASOs."));
  }, []);

  return (
    <div>
      <h2>ASOs</h2>
      {erro && <p style={{ color: "crimson" }}>{erro}</p>}
      <pre>{JSON.stringify(dados, null, 2)}</pre>
    </div>
  );
}
