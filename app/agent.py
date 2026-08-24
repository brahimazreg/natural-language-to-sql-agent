from app.llm import generate_sql
from app.sql_validator import validate_sql
from app.database import execute_sql


def generate_approved_sql(question: str):
    generated_sql = generate_sql(question)
    return validate_sql(generated_sql)


def run_agent(question: str):
    generated_sql = generate_sql(question)
    approved_sql = validate_sql(generated_sql)

    return execute_sql(approved_sql)