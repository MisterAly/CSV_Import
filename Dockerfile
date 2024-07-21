# Use a imagem base apropriada
FROM python:3.9-slim

# Defina variáveis de ambiente
ENV DEBIAN_FRONTEND=noninteractive

# Atualize os pacotes e instale dependências
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    gnupg \
    unixodbc-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instale a biblioteca psycopg2 para PostgreSQL
RUN pip install psycopg2-binary

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o código da aplicação para o contêiner
COPY . .

# Comando padrão para executar a aplicação Python
CMD ["python3", "seu_script.py"]
