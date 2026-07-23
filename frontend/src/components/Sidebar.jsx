import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Dashboard" },
  { to: "/funcionarios", label: "Funcionários" },
  { to: "/epis", label: "Fichas de EPI" },
  { to: "/asos", label: "ASO" },
  { to: "/nrs", label: "Normas Regulamentadoras" },
  { to: "/cats", label: "CAT" },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <h1>SST Manager</h1>
      <nav>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === "/"}
            style={({ isActive }) => ({
              backgroundColor: isActive ? "#2b527f" : "transparent",
              color: "white",
            })}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
