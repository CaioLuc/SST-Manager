# Como Contribuir

Guia essencial para desenvolvedores que farão manutenções, correções ou melhorias no projeto SST Manager.

> [!IMPORTANT]
> Certifique-se de alinhar o desenvolvimento de novas *features* com as arquiteturas detalhadas em [ARCHITECTURE.md](file:///c:/Projetos%20Faculdade/SST-Manager/ARCHITECTURE.md) e [FRONTEND.md](file:///c:/Projetos%20Faculdade/SST-Manager/FRONTEND.md).

## Pré-requisitos
Para rodar o ambiente de desenvolvimento, você precisará de:
- Python 3.11+
- Node.js 18+ e npm/yarn
- Docker e Docker Compose (para serviços auxiliares, como MySQL e Redis)

## Setup do Ambiente Local

### 1. Serviços de Infraestrutura (Docker)
Inicie o banco de dados e o cache na raiz do projeto:
```bash
docker compose up -d db redis
```

### 2. Backend (FastAPI)
```bash
cd backend
python -m venv venv
# Ativar venv:
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env # Ajuste as configurações, se necessário
alembic upgrade head # Cria as tabelas
uvicorn app.main:app --reload
```

### 3. Frontend (React/Vite)
```bash
cd frontend
npm install
cp .env.example .env # Verifique a variável VITE_API_URL (geralmente http://localhost:8000)
npm run dev
```

## Convenções de Código

### Python (Backend)
- Seguir o **PEP 8** rigorosamente.
- Uso mandatório de **Type Hints** em todas as funções e métodos.
- O idioma para nomes de classes relativas ao negócio pode ser Português (ex: `Funcionario`, `CriarAsoSchema`), mas variáveis estruturais devem manter padrão (ex: `db`, `session`, `router`).
- Utilize docstrings em português.

### JavaScript/React (Frontend)
- Utilização estrita de **Componentes Funcionais** e **Hooks**.
- Seguir validações do **ESLint** e uso de Prettier para formatação.

## Fluxo Git e Conventional Commits

1. **Branches**: Crie branches a partir da `main` no formato:
   - `feature/nome-da-funcionalidade`
   - `fix/nome-da-correcao`
   - `docs/nome-da-documentacao`
2. **Commits**: Utilizamos Conventional Commits em português.
   - `feat: adiciona CRUD de funcionarios`
   - `fix: corrige validacao do token JWT`
   - `docs: atualiza documentacao do banco`

## Checklist para Pull Requests

Antes de abrir o PR, garanta que:
- [ ] O código segue as convenções estilísticas citadas acima.
- [ ] Novas dependências foram adicionadas no `requirements.txt` ou `package.json`.
- [ ] Testes unitários / de integração passam e cobrem a nova funcionalidade (se aplicável).
- [ ] O banco de dados foi migrado com sucesso e scripts do Alembic foram gerados (se houver alteração de DB).
