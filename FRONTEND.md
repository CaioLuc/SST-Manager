# Arquitetura e Padrões do Frontend

Este documento descreve a organização e os padrões de projeto adotados no frontend React/Vite.

> [!TIP]
> Focamos no uso de componentes funcionais do React e hooks para manter o código limpo e moderno.

## Estrutura de Diretórios (Frontend)

```text
frontend/
├── src/
│   ├── assets/         # Imagens estáticas, ícones e fontes globais
│   ├── components/     # Componentes reutilizáveis (Botões, Inputs, Modais)
│   ├── pages/          # Componentes de página (Views completas associadas a rotas)
│   ├── services/       # Integrações de API (instância Axios, chamadas de endpoint)
│   ├── context/        # React Context (AuthContext, ThemeContext)
│   ├── utils/          # Funções de utilidade e formatação (data, moeda)
│   ├── App.jsx         # Componente raiz, onde as rotas são injetadas
│   └── main.jsx        # Ponto de entrada do Vite, renderização React DOM
├── index.html          # Template HTML principal
└── vite.config.js      # Configurações do Vite
```

## Design System

Mantemos uma interface moderna, consistente e "premium".
- **Tipografia**: Utilizamos a fonte **Inter** (do Google Fonts) como fonte principal para melhor legibilidade.
- **Paleta de Cores (Exemplo de Padrão)**:
  - Primária (Ações e Links): Azul moderno (ex: `#2563EB`)
  - Secundária (Destaques e Alertas): Verde (ex: `#10B981`) ou Laranja (ex: `#F59E0B`)
  - Fundo/Backgrounds: Tons neutros e suaves para evitar fadiga visual em uso prolongado (ex: `#F3F4F6`).

## Integração com API (Axios)

Toda a comunicação com o backend passa por instâncias pré-configuradas do `axios` na pasta `services/`.
- O `baseURL` é dinâmico e obtido via variáveis de ambiente (`import.meta.env.VITE_API_URL`).
- **Interceptors** são configurados para anexar automaticamente o cabeçalho `Authorization: Bearer <token>` caso o usuário esteja autenticado, e para interceptar erros `401 Unauthorized` executando o fluxo de refresh token ou redirecionamento para o login.

## Gerenciamento de Estado

- **Local State**: Uso padrão de `useState` e `useReducer` para controle de formulários e estados puramente locais.
- **Global State**: Evitamos bibliotecas complexas como Redux. O estado de autenticação e dados do tenant são gerenciados através da Context API (`AuthContext`).
- **Data Fetching**: Preferência pelo uso de hooks customizados associados a chamadas via Axios. (Uso futuro de React Query / SWR é recomendado para cacheamento complexo no client-side).

## Roteamento

O roteamento é controlado via **React Router v6**.
As rotas são divididas entre **públicas** (como `/login`, `/register`) e **protegidas**. Um componente wrapper `ProtectedRoute` encapsula as páginas da aplicação para garantir que usuários não autenticados sejam barrados de visualizá-las.

## Páginas Principais

- **`/` (Dashboard)**: Resumo geral, gráficos e alertas de vencimentos.
- **`/funcionarios`**: Tabela com paginação, filtros e botões para ações CRUD.
- **`/epi` / `/aso` / `/cat`**: Telas de formulários específicos e listagens correspondentes.
