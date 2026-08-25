from app.llm import generate_sql, regenerate_sql
from app.schema_loader import extract_schema
from app.sql_validator import validate_sql
from app.database import execute_sql
from app.validate_schema import validate_schema
from app.question_validator import validate_question_support




MAX_SQL_ATTEMPTS = 3


def generate_approved_sql(question: str) -> str:
    """
    Generate SQL and validate it.

    If validation fails, regenerate up to MAX_SQL_ATTEMPTS times.
    """

    schema = extract_schema()

    # --------------------------------------------------
    # Step 1: Validate the natural-language request
    # --------------------------------------------------

    supported, error = validate_question_support(
        question,
        schema,
    )

    if not supported:
        raise ValueError(error)

    # --------------------------------------------------
    # Step 2: Generate SQL
    # --------------------------------------------------

    generated_sql = generate_sql(question)

    last_error = None

    # --------------------------------------------------
    # Step 3: Validate / regenerate SQL
    # --------------------------------------------------

    for attempt in range(1, MAX_SQL_ATTEMPTS + 1):

        try:
            validate_sql(generated_sql)

            valid, error = validate_schema(
                generated_sql,
                schema,
            )

            if not valid:
                raise ValueError(error)

            return generated_sql

        except ValueError as exc:

            last_error = str(exc)

            if attempt == MAX_SQL_ATTEMPTS:
                raise ValueError(
                    f"SQL generation failed after "
                    f"{MAX_SQL_ATTEMPTS} attempts: {last_error}"
                ) from exc

            generated_sql = regenerate_sql(
                question=question,
                previous_sql=generated_sql,
                validation_error=last_error,
            )

    raise ValueError(
        f"SQL generation failed after "
        f"{MAX_SQL_ATTEMPTS} attempts."
    )


def run_agent(question: str):
    approved_sql = generate_approved_sql(question)
    print("QUESTION:", question)
    print("APPROVED SQL:", approved_sql)

    return execute_sql(approved_sql)