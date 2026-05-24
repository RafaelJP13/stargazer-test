# 🍀 Stargazer — Backend Técnico

API REST em Python (FastAPI) para gestão de clientes e integração simulada com Pipefy via GraphQL.

---

## 🧰 Tecnologias

- 🐍 Python 3.12
- ⚡ FastAPI + Uvicorn
- 🗄️ SQLAlchemy + PostgreSQL
- ✅ Pydantic v2
- 🧪 Pytest
- 🐳 Docker + Docker Compose

---

## ▶️ Como executar

### 📋 Pré-requisitos

- Docker
- Docker Compose

---

### ⚙️ 1. Clone o repositório e configure o ambiente

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

---

### 🐳 2. Suba os containers

```bash
docker-compose up --build
```

---

### 🌐 Acesse a aplicação

API:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

## 🧪 Como rodar os testes

Com os containers rodando:

```bash
docker-compose exec api pytest app/tests/ -v
```

### 📊 Cobertura de testes

```bash
docker-compose exec api pytest app/tests/ -v --cov=app --cov-report=term-missing
```

---

## 🗂️ Testes implementados

### 🔬 Unitários (13)

**👤 Cliente — serviço**
- ✅ Cria um cliente com sucesso
- ✅ Busca cliente por e-mail
- ✅ Retorna nulo quando cliente não existe
- ✅ Atualiza status e prioridade do cliente

**🗄️ Cliente — repositório**
- ✅ Atualiza um cliente no banco

**📋 Evento — repositório**
- ✅ Retorna verdadeiro quando evento já existe
- ✅ Retorna falso quando evento não existe

**🔁 Idempotência**
- ✅ Bloqueia processamento duplicado do mesmo evento

**💰 Regras de prioridade**
- ✅ Define prioridade alta quando patrimônio é exatamente R$ 200.000
- ✅ Define prioridade normal quando patrimônio é menor que R$ 200.000

**🔔 Webhook — serviço**
- ✅ Processa webhook com prioridade alta
- ✅ Processa webhook com prioridade normal

**⚠️ Webhook — erros**
- ✅ Retorna nulo quando cliente não é encontrad

## 🐞 Ferramenta de Debug da Integração Pipefy

O projeto inclui um utilitário interativo para inspeção e visualização das mutations GraphQL utilizadas na integração com Pipefy.

### ✨ A ferramenta permite

- simular o fluxo de criação de cards (`createCard`)
- simular atualização de campos (`updateCardField`)
- visualizar payloads GraphQL
- validar regras de prioridade
- inspecionar o fluxo de webhook
- debugar a integração localmente

---

### ▶️ Executar com Docker Compose

```bash
docker-compose exec api python pipefy_debug.py
```

---

### 🔀 Fluxos disponíveis

#### 🧾 Fluxo de criação de cliente

```bash
docker-compose exec api python pipefy_debug.py --mode create
```

#### 📦 Output JSON puro

```bash
docker-compose exec api python pipefy_debug.py --json
```

---

## 📡 Exemplos de requisição

### 👤 POST /clientes — Criar cliente

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

### ✅ Resposta esperada (`201 Created`)

```json
{
  "id": 1,
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "status": "Aguardando Análise"
}
```

---

### 🔔 POST /webhooks/pipefy/card-updated — Simular webhook do Pipefy

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

### ✅ Resposta esperada (`200 OK`)

Prioridade:
- `prioridade_alta`
- `prioridade_normal`

```json
{
  "message": "Card atualizado com sucesso",
  "status": "Processado",
  "prioridade": "prioridade_alta"
}
```

---

## ☁️ Visão de Produção (AWS) — Opcional

### 🚪 API Gateway + Lambda

Cada endpoint (`/clientes` e `/webhooks/pipefy/card-updated`) poderia se tornar uma função Lambda invocada pelo API Gateway, eliminando a necessidade de gerenciar servidores manualmente.

---

### 🗄️ RDS (PostgreSQL)

O banco local seria substituído por uma instância RDS Multi-AZ para:

- alta disponibilidade
- failover automático
- backups gerenciados

---

### 📨 SQS entre webhook e processamento

O webhook publicaria eventos em uma fila SQS, enquanto uma Lambda separada faria o processamento.

Benefícios:

- desacoplamento
- tolerância a picos
- retries automáticos
- redução de perda de eventos

---

### ⚡ DynamoDB para idempotência

A tabela de `events` poderia migrar para DynamoDB, aproveitando:

- baixa latência
- alta escalabilidade
- TTL nativo
- ótimo desempenho para chave única (`event_id`)

---

### 🔐 AWS Secrets Manager

Credenciais e tokens seriam armazenados no Secrets Manager, evitando exposição de segredos em variáveis de ambiente ou containers.

---

## 📌 Observações

- As integrações GraphQL seguem o padrão da documentação oficial do Pipefy.
- O envio ao Pipefy é simulado localmente conforme solicitado no teste técnico.
- O projeto utiliza persistência local com PostgreSQL via Docker Compose.
- Os testes automatizados cobrem:
  - criação de cliente
  - processamento de webhook
  - idempotência de eventos
