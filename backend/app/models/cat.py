from datetime import date
from sqlalchemy import String, Date, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CAT(Base):
    __tablename__ = "cats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    funcionario_id: Mapped[int] = mapped_column(ForeignKey("funcionarios.id"), nullable=False)
    numero_cat: Mapped[str] = mapped_column(String(50), nullable=True)
    data_acidente: Mapped[date] = mapped_column(Date, nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    parte_afetada: Mapped[str] = mapped_column(String(100), nullable=True)
    houve_afastamento: Mapped[bool] = mapped_column(default=False)

    funcionario = relationship("Funcionario", back_populates="cats")
