from datetime import date
from pydantic import BaseModel, ConfigDict


class FuncionarioBase(BaseModel):
    nome: str
    cpf: str
    matricula: str
    cargo: str
    setor: str
    data_admissao: date
    ativo: bool = True


class FuncionarioCreate(FuncionarioBase):
    pass


class FuncionarioUpdate(BaseModel):
    nome: str | None = None
    cargo: str | None = None
    setor: str | None = None
    ativo: bool | None = None


class FuncionarioOut(FuncionarioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
