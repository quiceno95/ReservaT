FROM python:3.11-slim

WORKDIR /app

# Set PYTHONPATH to include the src directory
ENV PYTHONPATH=/app/src

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Configurar AWS
ENV AWS_DEFAULT_REGION=us-east-1
ENV AWS_ACCESS_KEY_ID=AKIAWS2H4RB43LWZCISN
ENV AWS_SECRET_ACCESS_KEY=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
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Limpiar dependencias del sistema
RUN apt-get purge -y gcc && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

COPY . .

# Exponer el puerto correcto (8007)
EXPOSE 8007

# Configurar uvicorn para producción en el puerto correcto
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8007", "--workers", "2"]
