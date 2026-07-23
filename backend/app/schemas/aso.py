from datetime import date
from pydantic import BaseModel, ConfigDict
from app.models.aso import TipoASO, ResultadoASO


class ASOBase(BaseModel):
    funcionario_id: int
    tipo: TipoASO
    resultado: ResultadoASO
    data_exame: date
    data_validade: date


class ASOCreate(ASOBase):
    pass


class ASOOut(ASOBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
