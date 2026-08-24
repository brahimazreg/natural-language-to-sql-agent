from app.llm import generate_sql
from app.schema_loader import extract_schema
from app.sql_validator import validate_sql
from app.database import execute_sql
from app.validate_schema import validate_schema


def generate_approved_sql(question: str):
    generated_sql = generate_sql(question)
    return validate_sql(generated_sql)


def run_agent(question: str):
    generated_sql = generate_sql(question)

    validate_sql(generated_sql)

    schema = extract_schema()

    valid, error = validate_schema(
    generated_sql,
    schema,
    )

    if not valid:
        raise ValueError(error)

    return execute_sql(generated_sql)
