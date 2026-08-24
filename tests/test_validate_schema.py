from app.schema_loader import extract_schema
from app.validate_schema import validate_schema


def test_valid_select():
    schema = extract_schema()

    sql = """
        SELECT id, first_name, last_name
        FROM students
    """

    valid, error = validate_schema(sql, schema)

    assert valid is True
    assert error == ""


def test_invalid_table():
    schema = extract_schema()

    sql = """
        SELECT *
        FROM nonexistent_table
    """

    valid, error = validate_schema(sql, schema)

    assert valid is False
    assert "nonexistent_table" in error


def test_invalid_column():
    schema = extract_schema()

    sql = """
        SELECT email
        FROM students
    """

    valid, error = validate_schema(sql, schema)

    assert valid is False
    assert "email" in error


def test_valid_join():
    schema = extract_schema()

    sql = """
        SELECT
            p.name,
            s.first_name
        FROM programs p
        JOIN students s
            ON p.id = s.program_id
    """

    valid, error = validate_schema(sql, schema)

    assert valid is True
    assert error == ""


def test_invalid_join_column():
    schema = extract_schema()

    sql = """
        SELECT
            p.name,
            s.first_name
        FROM programs p
        JOIN students s
            ON p.id = s.program_id
        WHERE s.email = 'test@example.com'
    """

    valid, error = validate_schema(sql, schema)

    assert valid is False
    assert "email" in error

def test_realistic_average_exam_score_query():
    schema = extract_schema()

    sql = """
        SELECT
            c.id,
            c.code,
            c.name,
            AVG(er.score) AS average_score
        FROM courses c
        JOIN exams e
            ON c.id = e.course_id
        JOIN exam_results er
            ON e.id = er.exam_id
        GROUP BY c.id, c.code, c.name
    """

    valid, error = validate_schema(sql, schema)

    assert valid is True
    assert error == ""

def test_reject_hallucinated_student_email():
    schema = extract_schema()

    sql = """
        SELECT
            s.id,
            s.first_name,
            s.email
        FROM students s
    """

    valid, error = validate_schema(sql, schema)

    assert valid is False
    assert "email" in error