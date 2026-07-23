from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.models.user import RoleEnum

class UserBase(BaseModel):
    nome: str = Field(..., max_length=150)
    email: EmailStr
    role: RoleEnum = Field(default=RoleEnum.visualizador)
    ativo: bool = True

class UserCreate(UserBase):
    tenant_id: int
    password: str = Field(..., min_length=6)

class UserOut(UserBase):
    id: int
    tenant_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
