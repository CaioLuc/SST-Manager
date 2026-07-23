from datetime import date
from pydantic import BaseModel, ConfigDict


class CATBase(BaseModel):
    funcionario_id: int
    numero_cat: str | None = None
    data_acidente: date
    descricao: str
    parte_afetada: str | None = None
    houve_afastamento: bool = False


class CATCreate(CATBase):
    pass


class CATOut(CATBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
