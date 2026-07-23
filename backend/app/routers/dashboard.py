from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_tenant, require_role
from app.models.funcionario import Funcionario
from app.models.aso import ASO
from app.models.cat import CAT
from app.models.nr import NormaRegulamentadora

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/resumo", dependencies=[Depends(get_current_user), Depends(require_role("admin", "gestor", "tecnico", "visualizador"))])
async def resumo_geral(db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    """Indicadores gerenciais consolidados de SST"""
    hoje = date.today()
    em_30_dias = hoje + timedelta(days=30)

    total_funcionarios = (
        await db.execute(select(func.count()).select_from(Funcionario).where(Funcionario.ativo == True, Funcionario.tenant_id == tenant_id))
    ).scalar()

    asos_vencendo = (
        await db.execute(select(func.count()).select_from(ASO).where(ASO.data_validade <= em_30_dias, ASO.tenant_id == tenant_id))
    ).scalar()

    total_cats_ano = (
        await db.execute(
            select(func.count()).select_from(CAT).where(func.year(CAT.data_acidente) == hoje.year, CAT.tenant_id == tenant_id)
        )
    ).scalar()

    nrs_vencidas = (
        await db.execute(select(func.count()).select_from(NormaRegulamentadora).where(NormaRegulamentadora.status == "vencido", NormaRegulamentadora.tenant_id == tenant_id))
    ).scalar()

    return {
        "total_funcionarios_ativos": total_funcionarios or 0,
        "asos_vencendo_30_dias": asos_vencendo or 0,
        "cats_registradas_ano": total_cats_ano or 0,
        "nrs_vencidas": nrs_vencidas or 0,
    }
