from datetime import datetime
from pydantic import BaseModel, Field
from app.models.tenant import PlanoEnum

class TenantBase(BaseModel):
    nome: str = Field(..., max_length=150)
    slug: str = Field(..., max_length=150)
    cnpj: str = Field(..., max_length=14)
    plano: PlanoEnum = Field(default=PlanoEnum.free)
    ativo: bool = True

class TenantCreate(TenantBase):
    pass

class TenantOut(TenantBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
