# Project Progress — Natural Language to SQL Agent

## Current Status

The database foundation, NL2SQL pipeline, schema-aware prompting, and SQL schema validation are implemented.

Latest test status:

**25 passed, 4 warnings**

Command:

```powershell
pytest
```

The warnings are Gemini/LangChain warnings and are not test failures.

---

## Completed

* [x] GitHub repository created
* [x] Python 3.11 virtual environment
* [x] Docker Compose PostgreSQL
* [x] PostgreSQL running on host port 5433
* [x] Database schema created
* [x] Realistic seed data created
* [x] `nl2sql_agent` PostgreSQL role created
* [x] Read-only permissions configured
* [x] Database initialization made reproducible with:

  * `01-init.sql`
  * `02-seed.sql`
  * `03-roles.sql`
* [x] Database connection verified
* [x] Read access verified
* [x] Write access manually verified
* [x] Database security tests implemented
* [x] SQL safety validator implemented
* [x] LLM integration implemented with Gemini
* [x] LLM generates PostgreSQL SQL from natural language
* [x] SQL validator connected to LLM
* [x] Database execution implemented
* [x] Agent connects LLM → validator → database
* [x] Pytest suite implemented
* [x] Dynamic database schema loader implemented
* [x] Schema tables and columns extracted dynamically with SQLAlchemy
* [x] Foreign-key relationships extracted dynamically
* [x] LLM schema formatter implemented
* [x] Schema-aware Gemini system prompt implemented
* [x] Realistic NL2SQL tests implemented
* [x] Filtering SQL generation tested
* [x] Aggregation SQL generation tested
* [x] Multi-table JOIN SQL generation tested
* [x] SQL schema validation implemented with SQLGlot
* [x] Schema validation tests implemented
* [x] Invalid tables detected
* [x] Invalid columns detected
* [x] Table aliases handled
* [x] Schema validation integrated into `agent.py`

---

## Actual Database Schema

### `programs`

* `id`
* `name`
* `department`

### `students`

* `id`
* `first_name`
* `last_name`
* `birth_date`
* `program_id`
* `enrollment_year`

### `courses`

* `id`
* `code`
* `name`
* `credits`
* `program_id`

### `enrollments`

* `id`
* `student_id`
* `course_id`
* `academic_year`
* `semester`

### `exams`

* `id`
* `course_id`
* `exam_date`
* `exam_type`

### `exam_results`

* `id`
* `exam_id`
* `student_id`
* `score`
* `passed`

### Relationships

* `students.program_id → programs.id`
* `courses.program_id → programs.id`
* `enrollments.student_id → students.id`
* `enrollments.course_id → courses.id`
* `exams.course_id → courses.id`
* `exam_results.exam_id → exams.id`
* `exam_results.student_id → students.id`

---

## Current Architecture

```text
User question
    ↓
agent.py
    ↓
generate_sql()
    ↓
schema_loader.py
    ↓
Schema-aware Gemini prompt
    ↓
Generated PostgreSQL SQL
    ↓
validate_sql()
    ↓
validate_schema()
    ↓
execute_sql()
    ↓
Read-only PostgreSQL
    ↓
Results
```

### Responsibilities

#### `app/llm.py`

* Loads the actual database schema.
* Formats the schema for the LLM.
* Provides schema to Gemini through the system prompt.
* Instructs Gemini to:

  * Generate PostgreSQL SQL.
  * Generate SELECT only.
  * Use only existing tables and columns.
  * Use documented relationships.
  * Never invent schema elements.
  * Return SQL only.

#### `app/schema_loader.py`

* Uses SQLAlchemy inspection.
* Dynamically extracts tables.
* Dynamically extracts columns.
* Dynamically extracts foreign-key relationships.
* Formats the schema for the LLM.

#### `app/sql_validator.py`

Application-level SQL safety validation.

Rejects:

* INSERT
* UPDATE
* DELETE
* DROP
* ALTER
* CREATE
* TRUNCATE
* Multiple statements
* Empty queries

Allows:

* SELECT

#### `app/validate_schema.py`

Validates generated SQL against the actual database schema.

Checks:

* Tables exist.
* Columns exist.
* Table aliases are resolved.
* Invalid/hallucinated columns are rejected.
* Invalid/hallucinated tables are rejected.

Uses SQLGlot with PostgreSQL parsing.

#### `app/database.py`

* Connects to PostgreSQL.
* Executes already-approved SQL.
* Does NOT perform SQL validation.
* Database user remains read-only.

#### `app/agent.py`

Current intended flow:

```text
generate_sql()
    ↓
validate_sql()
    ↓
validate_schema()
    ↓
execute_sql()
```

`execute_sql()` should remain free of application-level SQL validation.

---

## Tests

Current test count:

**25 passed**

### `tests/test_database.py`

* Database connection
* Current user
* Read access
* Database write protection

### `tests/test_database_exec.py`

* Approved SELECT execution

### `tests/test_llm.py`

Realistic NL2SQL generation:

* Students by enrollment year
* Average exam score by course
* Students who passed exams
* Student/program aggregation

### `tests/test_sql_validator.py`

* SELECT allowed
* INSERT rejected
* UPDATE rejected
* DELETE rejected
* DROP rejected
* ALTER rejected
* CREATE rejected
* TRUNCATE rejected
* Multiple statements rejected
* Empty queries rejected

### `tests/test_validate_schema.py`

* Valid SELECT
* Invalid table
* Invalid column
* Valid JOIN
* Invalid JOIN column
* Realistic multi-table query
* Hallucinated `students.email` rejected

### `tests/test_agent.py`

* Complete agent flow

---

## Important Architecture Decisions

### Do NOT put SQL validation back inside `execute_sql()`

Keep the separation:

```text
LLM
 ↓
Safety validator
 ↓
Schema validator
 ↓
Database
```

The PostgreSQL read-only role provides database-level defense in depth.

### Embeddings are NOT currently needed

The database schema is small enough to provide directly to Gemini.

Current approach:

```text
Dynamic schema introspection
        ↓
Schema formatting
        ↓
LLM prompt
```

Do not introduce embeddings/RAG unless the project later grows to a much larger schema or documentation set.

---

## Known Warnings

Current pytest output:

**25 passed, 4 warnings**

Warnings are from `langchain_google_genai` / Gemini:

* Gemini model uses fixed sampling defaults, so `temperature` is ignored.
* Automatic Function Calling (AFC) warning appears during direct model generation.

These are currently warnings, not test failures.

They can be cleaned up later.

---

# NEXT STEP

## Integrate and strengthen the complete agent validation flow

Before moving to UI/API, verify that the complete pipeline reliably handles:

```text
Natural language
    ↓
Gemini
    ↓
Safety validation
    ↓
Schema validation
    ↓
PostgreSQL
```

### Tasks

* [ ] Review `app/agent.py`
* [ ] Make `generate_approved_sql()` perform BOTH:

  * `validate_sql()`
  * `validate_schema()`
* [ ] Make `run_agent()` use `generate_approved_sql()`
* [ ] Add agent-level test for invalid/hallucinated columns
* [ ] Add agent-level test for invalid/hallucinated tables
* [ ] Add end-to-end tests for realistic questions
* [ ] Confirm invalid SQL never reaches database execution
* [ ] Run full `pytest`
* [ ] Keep all tests passing

## After that

Investigate SQL regeneration/retry:

```text
Question
   ↓
Gemini
   ↓
SQL
   ↓
Safety validation
   ↓
Schema validation
   ↓
 ┌───────────────┐
 │ Valid?        │
 └───────┬───────┘
     No  │  Yes
         ↓
   Regenerate SQL       PostgreSQL
```

Only after NL2SQL reliability is strong should the project move toward:

* Result formatting
* API
* UI
* Deployment

## Resume Instruction

Tomorrow, say:

**"Resume Natural Language to SQL Agent from PROGRESS.md. We finished with 25 tests passing. Continue from NEXT STEP: strengthen the complete agent validation flow."**
