# Usa imagem oficial Python 3.12
FROM python:3.12-slim

# Atualiza pacotes básicos do sistema
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Diretório do app
WORKDIR /app

# Copia arquivos para a raiz
COPY requirements.txt .
COPY app.py .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Porta padrão do Gradio
EXPOSE 7860

# Comando para iniciar Gradio
CMD ["python", "app.py"]
