from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_tenant, require_role
from app.models.aso import ASO
from app.schemas.aso import ASOCreate, ASOOut

router = APIRouter(prefix="/asos", tags=["ASO"])


@router.get("/", response_model=list[ASOOut], dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico", "visualizador"))])
async def listar_asos(db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    result = await db.execute(select(ASO).where(ASO.tenant_id == tenant_id))
    return result.scalars().all()


@router.get("/vencendo", response_model=list[ASOOut], dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico", "visualizador"))])
async def asos_vencendo(dias: int = 30, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    """Retorna ASOs com validade vencendo nos próximos N dias (padrão 30)"""
    limite = date.today() + timedelta(days=dias)
    result = await db.execute(select(ASO).where(ASO.data_validade <= limite, ASO.tenant_id == tenant_id))
    return result.scalars().all()


@router.post("/", response_model=ASOOut, status_code=201, dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico"))])
async def criar_aso(dados: ASOCreate, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    novo = ASO(**dados.model_dump())
    novo.tenant_id = tenant_id
    db.add(novo)
    await db.commit()
    await db.refresh(novo)
    return novo


@router.delete("/{aso_id}", status_code=204, dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor"))])
async def remover_aso(aso_id: int, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    aso = await db.get(ASO, aso_id)
    if not aso or aso.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="ASO não encontrado")
    await db.delete(aso)
    await db.commit()
