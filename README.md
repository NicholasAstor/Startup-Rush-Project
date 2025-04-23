# Desafio IT Academy

Guia de execução para o projeto do 'Startup Rush'

## Requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Execução

### Executar com Docker Compose

```bash
docker compose up --build
```

> O processo de build leva aproximadamente 1 minuto, e a inicialização completa leva cerca de 1 minuto 30 segundos. O backend (Django) inclui um delay de 15 segundos para garantir que o banco de dados esteja pronto.

### Acessar a aplicação

Uma vez que todos os contêineres estejam rodando, acesse a aplicação em:

```
http://localhost:8000
```

### Parar execução

Para parar os contêineres:

```bash
docker compose down -v
```

Para reiniciar os contêineres:

```bash
docker compose up
```
ou

```bash
docker compose up -d
```

## Estrutura da Aplicação

- **Frontend**: Interface web construída com HTML, CSS, e JavaScript
- **Backend**: API Django 
- **Banco de Dados**: MySQL 8.0