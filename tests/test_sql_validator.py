import pytest
from app.sql_validator import validate_sql



def test_allow_select():
    assert validate_sql("SELECT * FROM students")


def test_reject_insert():
    with pytest.raises(ValueError):
        validate_sql("INSERT INTO students VALUES (1, 'Bob')")


def test_reject_update():
    with pytest.raises(ValueError):
        validate_sql("UPDATE students SET name='Bob'")


def test_reject_delete():
    with pytest.raises(ValueError):
        validate_sql("DELETE FROM students")


def test_reject_drop():
    with pytest.raises(ValueError):
        validate_sql("DROP TABLE students")


def test_reject_multiple_statements():
    with pytest.raises(ValueError):
        validate_sql("SELECT * FROM students; DROP TABLE students")

def test_reject_empty_query():
    with pytest.raises(ValueError, match="Empty queries"):
        validate_sql("")
        
def test_reject_whitespace_query():
    with pytest.raises(ValueError, match="Empty queries"):
        validate_sql("   ")

def test_delete_is_rejected():
    with pytest.raises(ValueError):
        validate_sql("DELETE FROM students")

