from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    """
    Schema para requisição de login.
    """
    email: EmailStr
    password: str
    tenant_slug: str

class TokenResponse(BaseModel):
    """
    Schema para resposta com token JWT.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    """
    Schema para requisição de registro de um novo tenant e usuário administrador inicial.
    """
    tenant_name: str
    cnpj: str
    user_name: str
    email: EmailStr
    password: str
