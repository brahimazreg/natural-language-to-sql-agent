from app.database import execute_sql



def test_execute_select():
    results = execute_sql("SELECT * FROM students")

    assert results
    assert len(results) == 25


