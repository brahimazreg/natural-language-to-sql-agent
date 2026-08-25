from app.llm import generate_sql, regenerate_sql
from app.schema_loader import extract_schema
from app.sql_validator import validate_sql
from app.database import execute_sql
from app.validate_schema import validate_schema


MAX_SQL_ATTEMPTS = 3


def generate_approved_sql(question: str) -> str:
    """
    Generate SQL and validate it.

    If validation fails, regenerate up to MAX_SQL_ATTEMPTS times.
    """

    schema = extract_schema()

    generated_sql = generate_sql(question)

    for attempt in range(1, MAX_SQL_ATTEMPTS + 1):

        try:
            # Layer 1: SQL safety validation
            validate_sql(generated_sql)

            # Layer 2: database schema validation
            valid, error = validate_schema(
                generated_sql,
                schema,
            )

            if not valid:
                raise ValueError(error)

            return generated_sql

        except ValueError as exc:
            validation_error = str(exc)

            if attempt == MAX_SQL_ATTEMPTS:
                raise ValueError(
                    f"SQL generation failed after "
                    f"{MAX_SQL_ATTEMPTS} attempts: "
                    f"{validation_error}"
                ) from exc

            generated_sql = regenerate_sql(
                question=question,
                previous_sql=generated_sql,
                validation_error=validation_error,
            )

    raise RuntimeError("Unexpected SQL generation state")


def run_agent(question: str):
    approved_sql = generate_approved_sql(question)

    return execute_sql(approved_sql)