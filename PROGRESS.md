# Project Progress — Natural Language to SQL Agent

## Current Status

The database foundation and core NL2SQL pipeline are complete.

### Completed

- [x] GitHub repository created
- [x] Python 3.11 virtual environment
- [x] Docker Compose PostgreSQL
- [x] PostgreSQL running on host port 5433
- [x] Database schema created
- [x] Realistic seed data created
- [x] `nl2sql_agent` PostgreSQL role created
- [x] Read-only permissions configured
- [x] Database initialization made reproducible with:
  - `01-init.sql`
  - `02-seed.sql`
  - `03-roles.sql`
- [x] Database connection verified
- [x] Read access verified
- [x] Write access manually verified
- [x] Database security tests implemented
- [x] SQL validator implemented
- [x] LLM integration implemented with Gemini
- [x] LLM generates SQL from natural language
- [x] SQL validator connected to LLM
- [x] Database execution implemented
- [x] Agent connects LLM → validator → database
- [x] Pytest suite implemented

### Current Test Status

Latest test:

    16 passed, 2 warnings

Command:

    pytest

The warnings are Gemini/LangChain warnings and are not test failures.

## Current Architecture

User question
    ↓
agent.py
    ↓
generate_sql()
    ↓
validate_sql()
    ↓
execute_sql()
    ↓
Read-only PostgreSQL
    ↓
Results

### Current responsibilities

`app/llm.py`
- Generates SQL from natural-language questions.

`app/sql_validator.py`
- Allows SELECT.
- Rejects INSERT.
- Rejects UPDATE.
- Rejects DELETE.
- Rejects DROP.
- Rejects ALTER.
- Rejects CREATE.
- Rejects TRUNCATE.
- Rejects multiple statements.
- Rejects empty/whitespace queries.

`app/database.py`
- Connects to PostgreSQL.
- Executes already-approved SQL.
- Does NOT perform SQL validation.
- Database user is read-only, providing a second security layer.

`app/agent.py`
- Orchestrates the complete workflow.
- `generate_approved_sql()` generates and validates SQL.
- `run_agent()` generates SQL, validates it, and executes it.

## Tests

`tests/test_database.py`
- Database connection
- Current user
- Read access
- Database write protection

`tests/test_sql_validator.py`
- SELECT allowed
- Forbidden SQL operations rejected
- Multiple statements rejected
- Empty queries rejected

`tests/test_llm.py`
- LLM generates SQL

`tests/test_agent.py`
- Complete agent flow returns database results

`tests/test_database_exec.py`
- Approved SELECT executes successfully

## Important Architecture Decision

Do NOT put SQL validation back inside `execute_sql()`.

The intended separation is:

LLM → Validator → Database

The validator provides application-level protection.

The PostgreSQL read-only role provides database-level defense in depth.

## NEXT STEP

Improve the LLM prompt so the model is aware of the actual PostgreSQL database schema.

The next task should be:

1. Inspect the current database schema.
2. Define a schema description for the LLM.
3. Add the schema to the system prompt in `app/llm.py`.
4. Make the prompt explicitly instruct the model to:
   - Generate PostgreSQL SQL.
   - Only generate SELECT queries.
   - Use only existing tables/columns.
   - Return SQL only.
   - Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or TRUNCATE.
5. Add tests for realistic natural-language questions.
6. Run `pytest` and keep the suite passing.

Do NOT move to UI/API yet. First make the NL2SQL generation reliable and schema-aware.


Tomorrow, you can simply tell me:

Resume Natural Language to SQL Agent from PROGRESS.md. We finished with 16 tests passing. Continue from NEXT STEP: make the LLM prompt schema-aware.