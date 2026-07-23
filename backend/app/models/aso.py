from datetime import date
from enum import Enum as PyEnum
from sqlalchemy import Date, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TipoASO(str, PyEnum):
    ADMISSIONAL = "admissional"
    PERIODICO = "periodico"
    RETORNO_TRABALHO = "retorno_trabalho"
    MUDANCA_FUNCAO = "mudanca_funcao"
    DEMISSIONAL = "demissional"


class ResultadoASO(str, PyEnum):
    APTO = "apto"
    INAPTO = "inapto"


class ASO(Base):
    __tablename__ = "asos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    funcionario_id: Mapped[int] = mapped_column(ForeignKey("funcionarios.id"), nullable=False)
    tipo: Mapped[TipoASO] = mapped_column(Enum(TipoASO), nullable=False)
    resultado: Mapped[ResultadoASO] = mapped_column(Enum(ResultadoASO), nullable=False)
    data_exame: Mapped[date] = mapped_column(Date, nullable=False)
    data_validade: Mapped[date] = mapped_column(Date, nullable=False)

    funcionario = relationship("Funcionario", back_populates="asos")
