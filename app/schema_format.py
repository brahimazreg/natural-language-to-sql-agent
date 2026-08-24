

def format_schema(schema: dict) -> str:
    """Convert extracted schema into an LLM-friendly description."""

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