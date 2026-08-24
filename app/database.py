import psycopg
from app.config import settings


def get_connection() -> psycopg.Connection:
    return psycopg.connect(
        host=settings.database_host,
        port=settings.database_port,
        dbname=settings.database_name,
        user=settings.database_user,
        password=settings.database_password
    )

def execute_sql(sql: str):
    """Execute validated SQL against PostgreSQL."""

    #sql_validated = validate_sql(sql)

    conn = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(sql)
        results = cur.fetchall()

        cur.close()

        return results

    finally:
        if conn is not None:
            conn.close()