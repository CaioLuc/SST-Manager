from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_tenant, require_role
from app.models.epi import FichaEPI
from app.schemas.epi import FichaEPICreate, FichaEPIOut

router = APIRouter(prefix="/epis", tags=["Fichas de EPI"])


@router.get("/", response_model=list[FichaEPIOut], dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico", "visualizador"))])
async def listar_fichas(db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    result = await db.execute(select(FichaEPI).where(FichaEPI.tenant_id == tenant_id))
    return result.scalars().all()


@router.get("/funcionario/{funcionario_id}", response_model=list[FichaEPIOut], dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico", "visualizador"))])
async def listar_fichas_por_funcionario(funcionario_id: int, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    result = await db.execute(select(FichaEPI).where(FichaEPI.funcionario_id == funcionario_id, FichaEPI.tenant_id == tenant_id))
    return result.scalars().all()


@router.post("/", response_model=FichaEPIOut, status_code=201, dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico"))])
async def criar_ficha(dados: FichaEPICreate, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    nova = FichaEPI(**dados.model_dump())
    nova.tenant_id = tenant_id
    db.add(nova)
    await db.commit()
    await db.refresh(nova)
    return nova


@router.delete("/{ficha_id}", status_code=204, dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor"))])
async def remover_ficha(ficha_id: int, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    ficha = await db.get(FichaEPI, ficha_id)
    if not ficha or ficha.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Ficha de EPI não encontrada")
    await db.delete(ficha)
    await db.commit()
