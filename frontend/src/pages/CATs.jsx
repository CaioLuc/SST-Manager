import { useEffect, useState } from "react";
import api from "../services/api";

export default function CATs() {
  const [dados, setDados] = useState([]);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    api
      .get("/cats/")
      .then((res) => setDados(res.data))
      .catch(() => setErro("Não foi possível carregar os dados de CATs."));
  }, []);

  return (
    <div>
      <h2>CATs</h2>
      {erro && <p style={{ color: "crimson" }}>{erro}</p>}
      <pre>{JSON.stringify(dados, null, 2)}</pre>
    </div>
  );
}
