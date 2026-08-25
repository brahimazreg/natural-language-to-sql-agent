import re


def validate_question_support(question: str, schema: dict) -> tuple[bool, str]:
    """
    Check whether the natural-language question requests
    data that exists in the database schema.

    Returns:
        (True, "") if the request appears supported.
        (False, error_message) otherwise.
    """

    question_lower = question.lower()

    tables = schema["tables"]

    # --------------------------------------------------
    # Student-specific fields
    # --------------------------------------------------

    student_fields = {
        "email": ["email", "email address", "email addresses"],
        "phone": ["phone", "phone number", "phone numbers", "telephone"],
        "first_name": ["first name", "first names"],
        "last_name": ["last name", "last names", "surname", "surnames"],
        "birth_date": ["birth date", "date of birth", "birthday"],
        "enrollment_year": [
            "enrollment year",
            "year of enrollment",
        ],
    }

    if "student" in question_lower or "students" in question_lower:

        student_columns = tables.get("students", [])

        for column, phrases in student_fields.items():

            requested = any(
                phrase in question_lower
                for phrase in phrases
            )

            if requested and column not in student_columns:
                return (
                    False,
                    f"The database schema does not contain "
                    f"a '{column}' field for students."
                )

    return True, ""