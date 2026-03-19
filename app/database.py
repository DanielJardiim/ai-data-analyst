import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings


def get_connection():
    return psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
    )


def execute_query(sql: str) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            return [dict(row) for row in results]


def get_schema() -> dict:
    sql = """
        SELECT
            table_name,
            column_name,
            data_type
        FROM
            information_schema.columns
        WHERE
            table_schema = 'public'
        ORDER BY
            table_name,
            ordinal_position;
    """
    rows = execute_query(sql)

    schema = {}
    for row in rows:
        table = row["table_name"]
        if table not in schema:
            schema[table] = []
        schema[table].append(
            {
                "column": row["column_name"],
                "type": row["data_type"],
            }
        )

    return schema
