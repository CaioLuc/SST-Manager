# Referência da API

Este documento detalha os principais endpoints da API do SST Manager.

> [!NOTE]
> Todos os endpoints da API (exceto `/auth/register` e `/auth/login`) requerem um Bearer token válido no cabeçalho `Authorization`.

## 1. Autenticação (`/auth`)

| Método | Endpoint | Descrição | Auth Requerido |
|--------|----------|-----------|----------------|
| POST   | `/auth/register` | Cria uma nova conta e um novo tenant | Público |
| POST   | `/auth/login`    | Autentica usuário e retorna JWT tokens | Público |
| POST   | `/auth/refresh`  | Atualiza access token usando refresh token | Qualquer Role |
| GET    | `/auth/me`       | Retorna dados do usuário autenticado atual | Qualquer Role |

**Exemplo Request `/auth/login`:**
```json
{
  "email": "usuario@empresa.com",
  "password": "senha_segura123"
}
```

**Exemplo Response `/auth/login`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

## 2. Funcionários (`/api/funcionarios`)

> [!IMPORTANT]
> Todas as requisições deste módulo filtram implicitamente pelo `tenant_id` extraído do token JWT.

| Método | Endpoint | Descrição | Auth Requerido |
|--------|----------|-----------|----------------|
| GET    | `/api/funcionarios` | Lista funcionários. Query params: `ativo`, `setor` | admin, gestor, tecnico, visualizador |
| GET    | `/api/funcionarios/{id}` | Detalhes de um funcionário específico | admin, gestor, tecnico, visualizador |
| POST   | `/api/funcionarios` | Cria novo funcionário | admin, gestor, tecnico |
| PUT    | `/api/funcionarios/{id}` | Atualiza dados do funcionário | admin, gestor, tecnico |
| DELETE | `/api/funcionarios/{id}` | Soft delete do funcionário | admin, gestor |

## 3. EPIs (`/api/epis`)

| Método | Endpoint | Descrição | Auth Requerido |
|--------|----------|-----------|----------------|
| GET    | `/api/epis` | Lista registros de EPIs entregues | Qualquer Role |
| POST   | `/api/epis` | Registra nova entrega de EPI | admin, gestor, tecnico |

**Exemplo Request POST `/api/epis`:**
```json
{
  "funcionario_id": 15,
  "equipamento": "Capacete de Segurança Classe B",
  "ca": "12345",
  "data_entrega": "2023-10-01",
  "data_validade": "2024-10-01"
}
```

## 4. ASOs e Saúde Ocupacional (`/api/asos`)

| Método | Endpoint | Descrição | Auth Requerido |
|--------|----------|-----------|----------------|
| GET    | `/api/asos` | Lista ASOs emitidos | Qualquer Role |
| GET    | `/api/asos/vencendo` | Lista ASOs próximos do vencimento. Query: `dias` | admin, gestor, tecnico |
| POST   | `/api/asos` | Registra novo ASO | admin, gestor, tecnico |

## 5. Normas Regulamentadoras (`/api/nrs`)

| Método | Endpoint | Descrição | Auth Requerido |
|--------|----------|-----------|----------------|
| GET    | `/api/nrs` | Lista NRs acompanhadas e seu status | Qualquer Role |
| PUT    | `/api/nrs/{id}/status` | Atualiza status de conformidade | admin, gestor, tecnico |

## 6. Comunicação de Acidente de Trabalho (`/api/cats`)

| Método | Endpoint | Descrição | Auth Requerido |
|--------|----------|-----------|----------------|
| GET    | `/api/cats` | Lista registros de CAT | Qualquer Role |
| POST   | `/api/cats` | Registra um novo acidente de trabalho | admin, gestor, tecnico |

## 7. Dashboard (`/api/dashboard`)

| Método | Endpoint | Descrição | Auth Requerido |
|--------|----------|-----------|----------------|
| GET    | `/api/dashboard/resumo` | Retorna KPIs consolidados (ativos, ASOs, etc) | Qualquer Role |
