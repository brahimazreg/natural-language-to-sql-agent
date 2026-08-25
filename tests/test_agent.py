import pytest
import app.agent as agent


def test_run_agent():
    response = agent.run_agent("Show me all students")

    assert response is not None
    assert len(response) == 25


def test_agent_rejects_hallucinated_column(monkeypatch):
    generated_sql = """
        SELECT id, first_name, email
        FROM students
    """

    monkeypatch.setattr(
        agent,
        "generate_sql",
        lambda question: generated_sql,
    )

    # Keep regeneration invalid so the agent must eventually reject it.
    monkeypatch.setattr(
        agent,
        "regenerate_sql",
        lambda question, previous_sql, validation_error: generated_sql,
    )

    def fail_if_executed(sql):
        pytest.fail("Invalid SQL reached database execution")

    monkeypatch.setattr(
        agent,
        "execute_sql",
        fail_if_executed,
    )

    with pytest.raises(ValueError, match="email"):
        agent.run_agent("Show student emails")


def test_agent_rejects_hallucinated_table(monkeypatch):
    generated_sql = """
        SELECT *
        FROM nonexistent_table
    """

    monkeypatch.setattr(
        agent,
        "generate_sql",
        lambda question: generated_sql,
    )

    # Keep regeneration invalid so the agent must eventually reject it.
    monkeypatch.setattr(
        agent,
        "regenerate_sql",
        lambda question, previous_sql, validation_error: generated_sql,
    )

    def fail_if_executed(sql):
        pytest.fail("Invalid SQL reached database execution")

    monkeypatch.setattr(
        agent,
        "execute_sql",
        fail_if_executed,
    )

    with pytest.raises(ValueError, match="nonexistent_table"):
        agent.run_agent("Show data from the nonexistent table")


def test_agent_rejects_hallucinated_column_after_three_attempts(monkeypatch):
    generated_sql = """
        SELECT id, first_name, email
        FROM students
    """

    generate_calls = 0
    regenerate_calls = 0

    def fake_generate(question):
        nonlocal generate_calls
        generate_calls += 1
        return generated_sql

    def fake_regenerate(question, previous_sql, validation_error):
        nonlocal regenerate_calls
        regenerate_calls += 1
        return generated_sql

    monkeypatch.setattr(
        agent,
        "generate_sql",
        fake_generate,
    )

    monkeypatch.setattr(
        agent,
        "regenerate_sql",
        fake_regenerate,
    )

    def fail_if_executed(sql):
        pytest.fail("Invalid SQL reached database execution")

    monkeypatch.setattr(
        agent,
        "execute_sql",
        fail_if_executed,
    )

    with pytest.raises(ValueError, match="3 attempts"):
        agent.run_agent("Show student names")

    assert generate_calls == 1
    assert regenerate_calls == 2


def test_agent_regenerates_until_valid(monkeypatch):
    invalid_sql = """
        SELECT id, first_name, email
        FROM students
    """

    valid_sql = """
        SELECT id, first_name, last_name
        FROM students
    """

    regenerate_calls = 0

    monkeypatch.setattr(
        agent,
        "generate_sql",
        lambda question: invalid_sql,
    )

    def fake_regenerate(question, previous_sql, validation_error):
        nonlocal regenerate_calls

        regenerate_calls += 1

        # Make sure the validation error is actually passed
        # to the regeneration step.
        assert "email" in validation_error

        return valid_sql

    monkeypatch.setattr(
        agent,
        "regenerate_sql",
        fake_regenerate,
    )

    expected_results = [
        (1, "John", "Smith"),
        (2, "Jane", "Doe"),
    ]

    monkeypatch.setattr(
        agent,
        "execute_sql",
        lambda sql: expected_results,
    )

    result = agent.run_agent("Show student names")

    assert result == expected_results
    assert regenerate_calls == 1


def test_agent_rejects_unsafe_sql_during_retry(monkeypatch):
    unsafe_sql = """
        DELETE FROM students
    """

    regenerate_calls = 0

    monkeypatch.setattr(
        agent,
        "generate_sql",
        lambda question: unsafe_sql,
    )

    def fake_regenerate(question, previous_sql, validation_error):
        nonlocal regenerate_calls

        regenerate_calls += 1

        return unsafe_sql

    monkeypatch.setattr(
        agent,
        "regenerate_sql",
        fake_regenerate,
    )

    monkeypatch.setattr(
        agent,
        "execute_sql",
        lambda sql: pytest.fail(
            "Unsafe SQL reached database execution"
        ),
    )

    with pytest.raises(ValueError, match="3 attempts"):
        agent.run_agent("Delete students")

    # One initial generation + two regenerations.
    assert regenerate_calls == 2
def test_agent_rejects_unsupported_email_request(monkeypatch):
    monkeypatch.setattr(
        agent,
        "execute_sql",
        lambda sql: pytest.fail(
            "Unsupported request reached database execution"
        ),
    )

    with pytest.raises(ValueError, match="email"):
        agent.run_agent(
            "Show me student email addresses."
        )


def test_agent_rejects_unsupported_phone_request(monkeypatch):
    monkeypatch.setattr(
        agent,
        "execute_sql",
        lambda sql: pytest.fail(
            "Unsupported request reached database execution"
        ),
    )

    with pytest.raises(ValueError, match="phone"):
        agent.run_agent(
            "Show me student phone numbers."
        )
 
