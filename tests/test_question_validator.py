from app.schema_loader import extract_schema
from app.question_validator import validate_question_support


def test_student_first_name_supported():
    schema = extract_schema()

    valid, error = validate_question_support(
        "Show me student first names.",
        schema,
    )

    assert valid is True
    assert error == ""


def test_student_email_unsupported():
    schema = extract_schema()

    valid, error = validate_question_support(
        "Show me student email addresses.",
        schema,
    )

    assert valid is False
    assert "email" in error


def test_student_phone_unsupported():
    schema = extract_schema()

    valid, error = validate_question_support(
        "Show me student phone numbers.",
        schema,
    )

    assert valid is False
    assert "phone" in error


def test_student_last_name_supported():
    schema = extract_schema()

    valid, error = validate_question_support(
        "Show me student last names.",
        schema,
    )

    assert valid is True
    assert error == ""