# AI Data Analyst

Faça perguntas em linguagem natural e receba respostas inteligentes sobre seus dados.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![LLM](https://img.shields.io/badge/LLM-Groq%20LLaMA3-orange)

## O que é este projeto?

Um sistema que permite que qualquer pessoa faça perguntas sobre um banco de dados
em linguagem natural, sem precisar saber SQL.

**Exemplo:**

> "Qual foi o faturamento total dos pedidos concluídos?"

O sistema converte automaticamente a pergunta em SQL, executa no banco de dados
real e retorna uma resposta explicada em português.

## Como funciona

```
Pergunta em português
        ↓
   LLM gera SQL
        ↓
PostgreSQL executa
        ↓
  LLM explica resultado
        ↓
Resposta em português
```

## Tecnologias

- **Backend:** Python 3.12 + FastAPI
- **Banco de dados:** PostgreSQL 16
- **LLM:** Groq API (LLaMA 3.3 70B)
- **Containerização:** Docker + Docker Compose
- **Validação:** Pydantic v2

## Pré-requisitos

- Docker Desktop instalado
- Conta na [Groq](https://console.groq.com) (gratuita)

## Como rodar localmente

**1. Clone o repositório**

```bash
git clone https://github.com/DanielJardiim/ai-data-analyst.git
cd ai-data-analyst
```

**2. Configure as variáveis de ambiente**

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais:

```bash
DB_USER=analyst_user
DB_PASSWORD=analyst123
DB_NAME=analyst_db
DB_HOST=db
DB_PORT=5432

LLM_API_KEY=sua-chave-groq-aqui
LLM_MODEL=llama-3.3-70b-versatile
LLM_BASE_URL=https://api.groq.com/openai/v1
```

**3. Suba o ambiente**

```bash
docker compose up --build
```

**4. Acesse a documentação interativa**

```
http://localhost:8000/docs
```

## Endpoints

| Método | Rota      | Descrição                             |
| ------ | --------- | ------------------------------------- |
| GET    | `/health` | Status da API                         |
| GET    | `/schema` | Schema do banco de dados              |
| POST   | `/query`  | Faz uma pergunta em linguagem natural |

## Exemplo de uso

**Requisição:**

```json
POST /query
{
    "question": "Qual produto gerou mais receita?"
}
```

**Resposta:**

```json
{
  "question": "Qual produto gerou mais receita?",
  "sql": "SELECT p.nome, SUM(i.valor) as receita FROM itens_pedido i JOIN produtos p ON i.produto_id = p.id GROUP BY p.nome ORDER BY receita DESC LIMIT 1;",
  "results": [{ "nome": "Plano Enterprise", "receita": "4000.00" }],
  "explanation": "O produto que gerou mais receita foi o Plano Enterprise, com R$ 4.000,00 em vendas no total."
}
```

## Estrutura do projeto

```
ai-data-analyst/
├── app/
│   ├── config.py      # Configurações centralizadas
│   ├── database.py    # Conexão e queries no PostgreSQL
│   ├── llm.py         # Integração com o LLM
│   ├── models.py      # Modelos de dados (Pydantic)
│   └── main.py        # Endpoints FastAPI
├── db/
│   └── seed.sql       # Dados de exemplo
├── .env.example       # Template de configuração
├── docker-compose.yml # Orquestração dos containers
├── Dockerfile         # Build da imagem Python
└── requirements.txt   # Dependências Python
```

## Roadmap

- [ ] Interface de chat no frontend
- [ ] Suporte a múltiplos bancos de dados
- [ ] Histórico de conversas
- [ ] Autenticação de usuários
- [ ] Geração automática de gráficos
- [ ] Multi-tenant para SaaS

## Autor

Daniel Jardim — [GitHub](https://github.com/DanielJardiim)
