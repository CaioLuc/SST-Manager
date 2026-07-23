from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_tenant, require_role
from app.models.funcionario import Funcionario
from app.schemas.funcionario import FuncionarioCreate, FuncionarioOut, FuncionarioUpdate

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])


@router.get("/", response_model=list[FuncionarioOut], dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico", "visualizador"))])
async def listar_funcionarios(db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    result = await db.execute(select(Funcionario).where(Funcionario.tenant_id == tenant_id))
    return result.scalars().all()


@router.get("/{funcionario_id}", response_model=FuncionarioOut, dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico", "visualizador"))])
async def obter_funcionario(funcionario_id: int, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    funcionario = await db.get(Funcionario, funcionario_id)
    if not funcionario or funcionario.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario


@router.post("/", response_model=FuncionarioOut, status_code=201, dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico"))])
async def criar_funcionario(dados: FuncionarioCreate, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    novo = Funcionario(**dados.model_dump())
    novo.tenant_id = tenant_id
    db.add(novo)
    await db.commit()
    await db.refresh(novo)
    return novo


@router.put("/{funcionario_id}", response_model=FuncionarioOut, dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico"))])
async def atualizar_funcionario(
    funcionario_id: int, dados: FuncionarioUpdate, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)
):
    funcionario = await db.get(Funcionario, funcionario_id)
    if not funcionario or funcionario.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(funcionario, campo, valor)
    await db.commit()
    await db.refresh(funcionario)
    return funcionario


@router.delete("/{funcionario_id}", status_code=204, dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor"))])
async def remover_funcionario(funcionario_id: int, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    funcionario = await db.get(Funcionario, funcionario_id)
    if not funcionario or funcionario.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    await db.delete(funcionario)
    await db.commit()
