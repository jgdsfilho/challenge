# Etapa de build
FROM python:3.13-slim AS builder

# Instalação de dependências necessárias para Poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalação do Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adiciona o Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Configuração do diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependência
COPY pyproject.toml poetry.lock ./

# Instala as dependências sem criar o ambiente virtual
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

# Etapa final
FROM python:3.13-slim

# Copia apenas as dependências instaladas da etapa de build
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Configuração do diretório de trabalho
WORKDIR /app

# Copia o código da aplicação
COPY . .

# Criação de um usuário não-root para executar o container
RUN useradd -m appuser
USER appuser

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]