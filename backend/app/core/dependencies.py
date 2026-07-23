from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from typing import Callable

from app.core.database import get_db
from app.core.security import decode_token

# Assumiremos que estes modelos existem ou serão criados em app/models/
from app.models.user import User
from app.models.tenant import Tenant

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Valida o token JWT e retorna o usuário atual, verificando se ele está ativo.
    """
    credenciais_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credenciais_exception
    except JWTError:
        raise credenciais_exception
        
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credenciais_exception
        
    if hasattr(user, "is_active") and not getattr(user, "is_active", True):
        raise HTTPException(status_code=400, detail="Usuário inativo")
        
    return user

def get_current_tenant(current_user: User = Depends(get_current_user)) -> int:
    """
    Retorna o ID do tenant (inquilino) associado ao usuário atual.
    """
    if not hasattr(current_user, "tenant_id") or current_user.tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não possui um tenant associado."
        )
    return current_user.tenant_id

def require_role(*roles: str) -> Callable:
    """
    Dependência que verifica se a função (role) do usuário está entre as permitidas.
    Retorna uma exceção HTTP 403 caso não possua as permissões.
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if not hasattr(current_user, "role") or current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissões insuficientes para acessar este recurso."
            )
        return current_user
    return role_checker
