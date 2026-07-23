# SST Manager

O **SST Manager** é uma plataforma SaaS (Software as a Service) voltada para a gestão de Segurança e Saúde no Trabalho. Desenvolvido para simplificar a vida de clínicas especializadas e profissionais técnicos, o sistema unifica controles de EPIs, atestados (ASO), conformidades em NRs e registros de acidentes (CAT).

![Status do Build](https://img.shields.io/badge/build-passing-brightgreen) ![Versão do Python](https://img.shields.io/badge/python-3.11%2B-blue) ![Versão do React](https://img.shields.io/badge/react-18%2B-blue)

## Links Rápidos da Documentação

A documentação do projeto está dividida em arquivos focados e modulares para facilitar o entendimento por desenvolvedores e inteligências artificiais:

- 📖 [Visão Geral do Projeto (PROJECT.md)](file:///c:/Projetos%20Faculdade/SST-Manager/PROJECT.md)
- 🏗️ [Arquitetura do Sistema (ARCHITECTURE.md)](file:///c:/Projetos%20Faculdade/SST-Manager/ARCHITECTURE.md)
- 🔌 [Referência da API (API.md)](file:///c:/Projetos%20Faculdade/SST-Manager/API.md)
- 🗄️ [Banco de Dados (DATABASE.md)](file:///c:/Projetos%20Faculdade/SST-Manager/DATABASE.md)
- 🛡️ [Segurança e Auth (SECURITY.md)](file:///c:/Projetos%20Faculdade/SST-Manager/SECURITY.md)
- 🎨 [Frontend (FRONTEND.md)](file:///c:/Projetos%20Faculdade/SST-Manager/FRONTEND.md)
- 📈 [Escalabilidade (SCALING.md)](file:///c:/Projetos%20Faculdade/SST-Manager/SCALING.md)
- 🤝 [Como Contribuir (CONTRIBUTING.md)](file:///c:/Projetos%20Faculdade/SST-Manager/CONTRIBUTING.md)

## Tech Stack (Resumo)

- **Backend**: Python, FastAPI, SQLAlchemy Assíncrono (MySQL), Pydantic.
- **Frontend**: React, Vite, TailwindCSS (ou CSS Vanilla estruturado), Axios.
- **Infra / Database**: Docker, MySQL 8.0, Redis.

## Quick Start (Rodando Localmente)

Siga os passos rápidos abaixo para levantar o projeto na sua máquina. Para requisitos mais detalhados, confira o guia de contribuição.

### 1. Inicie a infraestrutura
```bash
docker compose up -d db redis
```

### 2. Inicie o Backend (FastAPI)
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # ou "source venv/bin/activate" em Unix
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### 3. Inicie o Frontend (React)
Em um novo terminal:
```bash
cd frontend
npm install
npm run dev
```

## Licença

Este projeto é desenvolvido para fins acadêmicos e corporativos. Todos os direitos reservados.
