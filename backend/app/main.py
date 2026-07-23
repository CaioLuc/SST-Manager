from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.routers import funcionarios, epis, asos, cats, nrs, dashboard, auth
from app.core.middleware import SecurityHeadersMiddleware

# Importa os models para que fiquem registrados no Base.metadata
from app.models import funcionario, epi, aso, cat, nr, tenant, user  # noqa: F401

app = FastAPI(
    title="SST Manager API",
    description="API para gestão de Segurança e Saúde no Trabalho (EPI, NR, ASO, CAT e mais)",
    version="1.0.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # Documentação alternativa
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityHeadersMiddleware)

app.include_router(auth.router)
app.include_router(funcionarios.router)
app.include_router(epis.router)
app.include_router(asos.router)
app.include_router(cats.router)
app.include_router(nrs.router)
app.include_router(dashboard.router)


@app.on_event("startup")
async def on_startup():
    """Cria as tabelas automaticamente no startup (uso em desenvolvimento).
    Em produção, prefira Alembic para migrações controladas."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/", tags=["Status"])
async def root():
    return {"status": "online", "servico": "SST Manager API"}
