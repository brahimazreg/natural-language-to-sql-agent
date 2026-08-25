import sqlglot

def validate_sql(sql: str) -> str:
    if not sql or not sql.strip():
        raise ValueError("Empty queries are not allowed")

    try:
        statements = sqlglot.parse(sql, read="postgres")
    except sqlglot.ParseError as exc:
        raise ValueError(f"Invalid SQL syntax: {exc}") from exc

    if len(statements) != 1:
        raise ValueError("Multiple SQL statements are not allowed")

    statement = statements[0]

    if statement.key != "select":
        raise ValueError("Only SELECT queries are allowed")

    return sql