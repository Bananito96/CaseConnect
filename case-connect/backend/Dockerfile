# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Installare le dipendenze di sistema necessarie
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiare e installare le dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-scaricare il modello
RUN python -c "from FlagEmbedding import BGEM3FlagModel; BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)"

# Copiare il codice dell'applicazione
COPY . .

# Impostare le variabili d'ambiente
ENV PORT=8080
ENV FLASK_APP=app/main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Esportare la porta
EXPOSE 8080

# Comando per avviare l'applicazione
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
