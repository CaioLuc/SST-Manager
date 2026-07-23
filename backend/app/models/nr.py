from datetime import date
from sqlalchemy import String, Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class NormaRegulamentadora(Base):
    """Cadastro e status de conformidade de cada NR aplicável à empresa"""
    __tablename__ = "normas_regulamentadoras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    codigo: Mapped[str] = mapped_column(String(10), nullable=False)  # ex: NR-6, NR-9
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="pendente")  # pendente, em_dia, vencido
    ultima_verificacao: Mapped[date] = mapped_column(Date, nullable=True)
    proxima_verificacao: Mapped[date] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str] = mapped_column(String(500), nullable=True)
