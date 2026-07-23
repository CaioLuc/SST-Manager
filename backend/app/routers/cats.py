from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_tenant, require_role
from app.models.cat import CAT
from app.schemas.cat import CATCreate, CATOut

router = APIRouter(prefix="/cats", tags=["CAT"])


@router.get("/", response_model=list[CATOut], dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico", "visualizador"))])
async def listar_cats(db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    result = await db.execute(select(CAT).where(CAT.tenant_id == tenant_id))
    return result.scalars().all()


@router.post("/", response_model=CATOut, status_code=201, dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico"))])
async def criar_cat(dados: CATCreate, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    nova = CAT(**dados.model_dump())
    nova.tenant_id = tenant_id
    db.add(nova)
    await db.commit()
    await db.refresh(nova)
    return nova


@router.delete("/{cat_id}", status_code=204, dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor"))])
async def remover_cat(cat_id: int, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    cat = await db.get(CAT, cat_id)
    if not cat or cat.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="CAT não encontrada")
    await db.delete(cat)
    await db.commit()
