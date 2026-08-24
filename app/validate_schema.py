import sqlglot
from sqlglot import exp


def validate_schema(sql: str, schema: dict) -> tuple[bool, str]:
    """
    Validate that tables and columns referenced by SQL
    exist in the database schema.

    Returns:
        (True, "") if valid
        (False, error_message) if invalid
    """

    try:
        tree = sqlglot.parse_one(sql, read="postgres")
    except sqlglot.ParseError as exc:
        return False, f"Invalid SQL syntax: {exc}"

    tables = schema["tables"]

    # --------------------------------------------------
    # 1. Validate table names
    # --------------------------------------------------

    referenced_tables = {}

    for table in tree.find_all(exp.Table):
        table_name = table.name

        if table_name not in tables:
            return False, f"Table '{table_name}' does not exist in database schema."

        alias = table.alias_or_name
        referenced_tables[alias] = table_name

    # --------------------------------------------------
    # 2. Validate column names
    # --------------------------------------------------

    for column in tree.find_all(exp.Column):
        column_name = column.name
        table_alias = column.table

        # Ignore wildcard:
        # SELECT *
        if column_name == "*":
            continue

        # Qualified column:
        # students.first_name
        if table_alias:
            if table_alias not in referenced_tables:
                return False, (
                    f"Table or alias '{table_alias}' "
                    f"does not exist in query."
                )

            actual_table = referenced_tables[table_alias]

            if column_name not in tables[actual_table]:
                return False, (
                    f"Column '{column_name}' does not exist "
                    f"in table '{actual_table}'."
                )

        # Unqualified column:
        # SELECT first_name FROM students
        else:
            matching_tables = [
                table_name
                for table_name in referenced_tables.values()
                if column_name in tables[table_name]
            ]

            if not matching_tables:
                return False, (
                    f"Column '{column_name}' does not exist "
                    f"in the referenced tables."
                )

    return True, ""