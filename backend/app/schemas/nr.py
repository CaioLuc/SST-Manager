from datetime import date
from pydantic import BaseModel, ConfigDict


class NRBase(BaseModel):
    codigo: str
    titulo: str
    status: str = "pendente"
    ultima_verificacao: date | None = None
    proxima_verificacao: date | None = None
    observacoes: str | None = None


class NRCreate(NRBase):
    pass


class NROut(NRBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
