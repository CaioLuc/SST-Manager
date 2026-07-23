from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import verify_password, hash_password, create_access_token, create_refresh_token, decode_token
from app.core.dependencies import get_current_user
from app.schemas.auth import LoginRequest, TokenResponse, RegisterRequest

# Assumiremos que estes modelos existem ou serão criados em app/models/
from app.models.user import User
from app.models.tenant import Tenant

router = APIRouter(prefix="/auth", tags=["auth"])

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Cria um novo tenant e um usuário administrador inicial, e retorna os tokens JWT.
    """
    # Verifica se já existe um tenant com o mesmo CNPJ
    tenant_existente = db.query(Tenant).filter(Tenant.cnpj == request.cnpj).first()
    if tenant_existente:
        raise HTTPException(status_code=400, detail="Já existe um tenant com este CNPJ")
        
    # Verifica se já existe um usuário com o mesmo email
    usuario_existente = db.query(User).filter(User.email == request.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Já existe um usuário com este e-mail")
        
    # Criação do tenant (assumindo slug baseado no nome ou recebido, aqui faremos simplificado)
    slug = request.tenant_name.lower().replace(" ", "-")
    novo_tenant = Tenant(
        name=request.tenant_name,
        cnpj=request.cnpj,
        slug=slug
    )
    db.add(novo_tenant)
    db.commit()
    db.refresh(novo_tenant)
    
    # Criação do usuário admin
    novo_usuario = User(
        name=request.user_name,
        email=request.email,
        hashed_password=hash_password(request.password),
        tenant_id=novo_tenant.id,
        role="admin",
        is_active=True
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    # Gerar tokens
    access_token = create_access_token(data={"sub": str(novo_usuario.id)})
    refresh_token = create_refresh_token(data={"sub": str(novo_usuario.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Valida as credenciais do usuário e retorna os tokens JWT (access_token e refresh_token).
    """
    # Verifica o tenant pelo slug
    tenant = db.query(Tenant).filter(Tenant.slug == request.tenant_slug).first()
    if not tenant:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tenant não encontrado")
        
    # Verifica o usuário
    user = db.query(User).filter(User.email == request.email, User.tenant_id == tenant.id).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos")
        
    if hasattr(user, "is_active") and not getattr(user, "is_active", True):
        raise HTTPException(status_code=400, detail="Usuário inativo")
        
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshRequest):
    """
    Aceita um refresh_token válido e retorna um novo access_token (e possivelmente um novo refresh_token).
    """
    try:
        payload = decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
            
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
            
        # Gera novos tokens
        new_access_token = create_access_token(data={"sub": user_id})
        new_refresh_token = create_refresh_token(data={"sub": user_id})
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado ou inválido")

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """
    Retorna o perfil do usuário logado atualmente.
    Requer autenticação.
    """
    return {
        "id": current_user.id,
        "name": getattr(current_user, "name", None),
        "email": getattr(current_user, "email", None),
        "role": getattr(current_user, "role", None),
        "tenant_id": getattr(current_user, "tenant_id", None)
    }
