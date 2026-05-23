# Stargazer — Backend Técnico
 
API REST em Python (FastAPI) para gestão de clientes e integração simulada com Pipefy via GraphQL.
 
## Tecnologias
 
- Python 3.12
- FastAPI + Uvicorn
- SQLAlchemy + PostgreSQL
- Pydantic v2
- Pytest
- Docker + Docker Compose
## Como executar
 
### Pré-requisitos
 
- Docker e Docker Compose instalados
### 1. Clone o repositório e configure o ambiente
 
Copie o `.env.example` para `.env` com as credenciais desejadas:
 
```env
APP_PORT=8000
DB_HOST=postgres
DB_PORT=5432
DB_NAME=postgres_db
DB_USER=postgres
DB_PASSWORD=postgres
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/postgres_db
```
 
### 2. Suba os containers
 
```bash
docker-compose up --build
```
 
A API estará disponível em `http://localhost:8000`.
 
Documentação interativa: `http://localhost:8000/docs`
 
---
 
## Como rodar os testes
 
Com os containers rodando:
 
```bash
docker-compose exec api pytest app/tests/ -v
```
 
Para ver cobertura:
 
```bash
docker-compose exec api pytest app/tests/ -v --cov=app --cov-report=term-missing
```
 
---
 
## Exemplos de requisição
 
### POST /clientes — Criar cliente
 
```bash
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": 250000
  }'
```
 
Resposta esperada (`201 Created`):
 
```json
{
  "id": 1,
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "status": "Aguardando Análise"
}
```
 
---
 
### POST /webhooks/pipefy/card-updated — Simular webhook do Pipefy
 
```bash
curl -X POST http://localhost:8000/webhooks/pipefy/card-updated \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_123",
    "card_id": "card_456",
    "cliente_email": "joao.silva@example.com",
    "timestamp": "2026-05-18T12:00:00Z"
  }'
```
 
Resposta esperada (`200 OK`):
 
```json
{
  "message": "Card atualizado com sucesso",
  "status": "Processado",
  "prioridade": "prioridade_alta" | "prioridade_normal"
}
```
 
---
 
## Visão de Produção (AWS) — Opcional
 
Para escalar essa estrutura na AWS:
 
- **API Gateway + Lambda**: cada endpoint (`/clientes` e `/webhooks/pipefy/card-updated`) se tornaria uma função Lambda invocada pelo API Gateway, eliminando a necessidade de gerenciar servidores.
- **RDS (PostgreSQL)**: o banco local seria substituído por uma instância RDS Multi-AZ para alta disponibilidade e failover automático.
- **SQS entre o webhook e o processamento**: o endpoint do webhook publicaria o evento numa fila SQS, e uma Lambda separada consumiria a fila — garantindo idempotência e desacoplamento, sem risco de perda de eventos em picos de carga.
- **DynamoDB para controle de eventos**: a tabela de `events` (idempotência por `event_id`) se beneficiaria do DynamoDB pela latência baixa em operações de leitura/escrita de chave única, além de TTL nativo para expirar eventos antigos.
- **Secrets Manager**: as credenciais do banco e tokens do Pipefy seriam armazenados no AWS Secrets Manager, sem expor variáveis de ambiente nos containers.
