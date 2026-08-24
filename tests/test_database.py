import psycopg
from app.database import get_connection


def test_database_connection():
    with get_connection() as connection:
        assert connection.execute("SELECT 1").fetchone() == (1,)


def test_database_user_is_read_only_agent():
    with get_connection() as connection:
        result = connection.execute(
            "SELECT current_user"
        ).fetchone()

        assert result[0] == "nl2sql_agent"


def test_database_read_access():
    with get_connection() as connection:
        result = connection.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()

        assert result[0] > 0


def test_database_write_is_forbidden():
    with get_connection() as connection:
        try:
            connection.execute(
                "DELETE FROM students"
            )
        except psycopg.errors.InsufficientPrivilege:
            pass
        else:
            raise AssertionError(
                "nl2sql_agent must not have write access"
            )


