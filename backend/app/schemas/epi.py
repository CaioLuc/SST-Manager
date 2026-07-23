from datetime import date
from pydantic import BaseModel, ConfigDict


class FichaEPIBase(BaseModel):
    funcionario_id: int
    equipamento: str
    certificado_aprovacao: str
    data_entrega: date
    data_validade: date | None = None
    assinatura_confirmada: bool = False


class FichaEPICreate(FichaEPIBase):
    pass


class FichaEPIOut(FichaEPIBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
