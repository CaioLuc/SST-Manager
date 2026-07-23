from datetime import date
from sqlalchemy import String, Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class FichaEPI(Base):
    __tablename__ = "fichas_epi"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    funcionario_id: Mapped[int] = mapped_column(ForeignKey("funcionarios.id"), nullable=False)
    equipamento: Mapped[str] = mapped_column(String(150), nullable=False)
    certificado_aprovacao: Mapped[str] = mapped_column(String(30), nullable=False)
    data_entrega: Mapped[date] = mapped_column(Date, nullable=False)
    data_validade: Mapped[date] = mapped_column(Date, nullable=True)
    assinatura_confirmada: Mapped[bool] = mapped_column(default=False)

    funcionario = relationship("Funcionario", back_populates="epis")
