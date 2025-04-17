# Escolhi essa versão do python por ser mais reduzido portanto mais leve
FROM python:3.10-slim

WORKDIR /client

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#Insatalando algumas dependências e removendo alguns arquivos, passo necessário para o funcionamento do projeto
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --upgrade pip wheel setuptools \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Entrypoint script foi necessário para conseguir rodar o projeto, não consegui fazer com o CMD direto
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
