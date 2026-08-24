from app.llm import generate_sql


def test_generate_sql_students_by_year():
    sql = generate_sql(
        "Show students who enrolled in 2024."
    )

    assert "SELECT" in sql.upper()
    assert "students" in sql.lower()
    assert "enrollment_year" in sql.lower()
    assert "2024" in sql


def test_generate_sql_average_exam_score_by_course():
    sql = generate_sql(
        "What is the average exam score for each course?"
    )

    assert "SELECT" in sql.upper()
    assert "courses" in sql.lower()
    assert "exams" in sql.lower()
    assert "exam_results" in sql.lower()
    assert "AVG" in sql.upper()


def test_generate_sql_students_who_passed():
    sql = generate_sql(
        "Which students passed their exams?"
    )

    assert "SELECT" in sql.upper()
    assert "students" in sql.lower()
    assert "exam_results" in sql.lower()
    assert "passed" in sql.lower()