from fastapi import FastAPI, HTTPException
from app.database import get_schema, execute_query
from app.llm import generate_sql, generate_explanation
from app.models import QueryRequest, QueryResponse

app = FastAPI(
    title="AI Data Analyst",
    description="Perguntas em linguagem natural sobre seus dados",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "API no ar",
        "version": "0.1.0",
    }


@app.get("/schema")
def read_schema():
    try:
        schema = get_schema()
        return {"schema": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        # Passo 1: busca o schema atual do banco
        schema = get_schema()

        # Passo 2: envia perguntas + schema para o LLM gerar o SQL
        sql = generate_sql(question=request.question, schema=schema)

        # Passo 3: executa o SQL no PostgreSQL
        results = execute_query(sql)

        # Passo 4: envia resultados para o LLM gerar explicação
        explanation = generate_explanation(
            question=request.question, sql=sql, results=results
        )

        return QueryResponse(
            question=request.question, sql=sql, results=results, explanation=explanation
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
