def validate_sql(sql: str) -> str:

    if len(sql.strip()) == 0:
        raise ValueError("Empty queries are not allowed")

    sql_upper = sql.strip().upper()

    forbidden = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "CREATE",
        "TRUNCATE",
    ]

    for word in forbidden:
        if word in sql_upper:
            raise ValueError(f"Forbidden SQL operation: {word}")

    if not sql_upper.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")

    return sql