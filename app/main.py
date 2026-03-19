from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_schema, execute_query
from app.llm import generate_sql, generate_explanation
from app.models import QueryRequest, QueryResponse

app = FastAPI(
    title="AI Data Analyst",
    description="Perguntas em linguagem natural sobre seus dados",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
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
        schema = get_schema()

        sql = generate_sql(
            question=request.question,
            schema=schema,
        )

        results = execute_query(sql)

        explanation = generate_explanation(
            question=request.question,
            sql=sql,
            results=results,
        )

        return QueryResponse(
            question=request.question,
            sql=sql,
            results=results,
            explanation=explanation,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
