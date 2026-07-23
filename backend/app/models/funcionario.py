from datetime import date
from sqlalchemy import String, Date, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Funcionario(Base):
    __tablename__ = "funcionarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    matricula: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    cargo: Mapped[str] = mapped_column(String(100), nullable=False)
    setor: Mapped[str] = mapped_column(String(100), nullable=False)
    data_admissao: Mapped[date] = mapped_column(Date, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    epis = relationship("FichaEPI", back_populates="funcionario", cascade="all, delete-orphan")
    asos = relationship("ASO", back_populates="funcionario", cascade="all, delete-orphan")
    cats = relationship("CAT", back_populates="funcionario", cascade="all, delete-orphan")
