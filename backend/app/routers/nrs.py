from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_tenant, require_role
from app.models.nr import NormaRegulamentadora
from app.schemas.nr import NRCreate, NROut

router = APIRouter(prefix="/nrs", tags=["Normas Regulamentadoras"])


@router.get("/", response_model=list[NROut], dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico", "visualizador"))])
async def listar_nrs(db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    result = await db.execute(select(NormaRegulamentadora).where(NormaRegulamentadora.tenant_id == tenant_id))
    return result.scalars().all()


@router.post("/", response_model=NROut, status_code=201, dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico"))])
async def criar_nr(dados: NRCreate, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    nova = NormaRegulamentadora(**dados.model_dump())
    nova.tenant_id = tenant_id
    db.add(nova)
    await db.commit()
    await db.refresh(nova)
    return nova


@router.delete("/{nr_id}", status_code=204, dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor"))])
async def remover_nr(nr_id: int, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    nr = await db.get(NormaRegulamentadora, nr_id)
    if not nr or nr.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Norma Regulamentadora não encontrada")
    await db.delete(nr)
    await db.commit()
