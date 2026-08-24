from sqlalchemy import create_engine, inspect
from app.config import settings

def get_connection_string() -> str:
    """Return database connection string for SQLAlchemy"""    
    return f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

def extract_schema():
    """Extract database tables, columns, and relationships."""

    connection_string = get_connection_string()
    engine = create_engine(connection_string)

    inspector = inspect(engine)

    schema = {
        "tables": {},
        "relationships": [],
    }

    for table in inspector.get_table_names():
        if table.lower() == "sysdiagrams":
            continue

        columns = inspector.get_columns(table)

        schema["tables"][table] = [
            col["name"]
            for col in columns
        ]

        foreign_keys = inspector.get_foreign_keys(table)

        for foreign_key in foreign_keys:
            referred_table = foreign_key["referred_table"]

            if referred_table.lower() == "sysdiagrams":
                continue

            for local_column, referred_column in zip(
                foreign_key["constrained_columns"],
                foreign_key["referred_columns"],
            ):
                schema["relationships"].append(
                    {
                        "from_table": table,
                        "from_column": local_column,
                        "to_table": referred_table,
                        "to_column": referred_column,
                    }
                )

    return schema

def format_schema(schema: dict) -> str:
    """Convert database schema into an LLM-friendly description."""

    lines = ["DATABASE SCHEMA:", ""]

    for table, columns in schema["tables"].items():
        lines.append(f"Table: {table}")

        for column in columns:
            lines.append(f"  - {column}")

        lines.append("")

    if schema["relationships"]:
        lines.append("RELATIONSHIPS:")

        for relationship in schema["relationships"]:
            lines.append(
                f"  - {relationship['from_table']}."
                f"{relationship['from_column']} -> "
                f"{relationship['to_table']}."
                f"{relationship['to_column']}"
            )

    return "\n".join(lines)