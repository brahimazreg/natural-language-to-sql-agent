import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from app.schema_loader  import extract_schema ,format_schema



load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

llm=ChatGoogleGenerativeAI(model = "models/gemini-3.5-flash-lite", temperature=0 )


def generate_sql(question: str) -> str:

    get_schema = extract_schema()
    schema = format_schema(get_schema)

    response = llm.invoke([
        (
            "system",
            f"""
You are a PostgreSQL SQL generation assistant.

Convert the user's natural-language question into a PostgreSQL SQL query.

DATABASE SCHEMA:
{schema}

The schema above is the complete database schema.

You MUST NOT use any table or column that is not explicitly listed.

Before returning SQL, verify every table name and every column name
against the schema.

Do not guess column names based on natural-language terminology.

Rules:
- Generate PostgreSQL-compatible SQL.
- Generate SELECT queries only.
- Use only tables and columns present in the schema.
- Never invent tables or columns.
- Use the documented relationships when joining tables.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or TRUNCATE.
- Return SQL only.
- Do not return markdown.
- Do not explain the SQL.
"""
        ),
        ("human", question),
    ])

    sql = response.content[0]["text"]

    return sql