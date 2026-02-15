# Usa imagem oficial Python 3.12
FROM python:3.12-slim

# Atualiza pacotes e instala dependências básicas
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Define diretório do app
WORKDIR /app

# Copia arquivos
COPY requirements.txt .
COPY app ./app

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Porta será definida dinamicamente pelo Fly.io
EXPOSE 8080

# Comando para iniciar FastAPI com a porta do ambiente
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
