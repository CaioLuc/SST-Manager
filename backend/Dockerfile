# ==========================================
# Estágio 1: Build e Instalação de Dependências
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Copia apenas o arquivo de dependências para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências em um diretório temporário isolado (/install)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==========================================
# Estágio 2: Imagem Final de Execução (Runtime)
# ==========================================
FROM python:3.11-slim

WORKDIR /app

# Criar usuário sem privilégios de root para segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copiar dependências compiladas/instaladas do estágio de builder
COPY --from=builder /install /usr/local

# Copiar os arquivos da aplicação
COPY . .

# Alternar para o usuário não-root
USER appuser

EXPOSE 8000

# Verificação de saúde da aplicação (Healthcheck)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# Comando de inicialização do servidor de aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
