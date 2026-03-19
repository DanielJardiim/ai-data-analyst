import httpx
from app.config import settings


def _build_schema_prompt(schema: dict) -> str:
    lines = []
    for table, columns in schema.items():
        cols = ", ".join(f"{col['column']} ({col['type']})" for col in columns)
        lines.append(f"- {table}: {cols}")
    return "\n".join(lines)


def _build_system_prompt(schema: dict) -> str:
    schema_text = _build_schema_prompt(schema)
    return f"""Você é um especialista em SQL e análise de dados.

Seu trabalho é converter perguntas em linguagem natural em queries SQL válidas para PostgreSQL.

O banco de dados possui as seguintes tabelas e colunas:
{schema_text}

Regras obrigatórias:
1. Responda APENAS com o SQL puro, sem explicações, sem markdown, sem blocos de código.
2. Não use ```sql ou ``` na resposta.
3. Use apenas as tabelas e colunas listadas acima.
4. Sempre termine o SQL com ponto e vírgula.
5. Para filtros de data use NOW() e INTERVAL do PostgreSQL.
6. Nunca use DELETE, DROP, UPDATE, INSERT ou ALTER — apenas SELECT.

Exemplo de resposta correta:
SELECT * FROM produtos WHERE categoria = 'assinatura';"""


def _build_explanation_prompt(question: str, sql: str, results: list) -> str:
    return f"""O usuário fez a seguinte pergunta: "{question}"

O SQL executado foi:
{sql}

Os resultados retornados foram:
{results}

Responda a pergunta do usuário em português brasileiro de forma clara e direta,
interpretando os dados retornados. Seja objetivo mas completo.
Não mencione o SQL na resposta."""


def generate_sql(question: str, schema: dict) -> str:
    system_prompt = _build_system_prompt(schema)

    response = httpx.post(
        url=f"{settings.llm_base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.llm_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": settings.llm_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            "temperature": 0,
            "max_tokens": 500,
        },
        timeout=30,
    )

    response.raise_for_status()
    data = response.json()
    sql = data["choices"][0]["message"]["content"].strip()
    return sql


def generate_explanation(question: str, sql: str, results: list) -> str:
    explanation_prompt = _build_explanation_prompt(question, sql, results)

    response = httpx.post(
        url=f"{settings.llm_base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.llm_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": settings.llm_model,
            "messages": [
                {"role": "user", "content": explanation_prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 500,
        },
        timeout=30,
    )

    response.raise_for_status()
    data = response.json()
    explanation = data["choices"][0]["message"]["content"].strip()
    return explanation
