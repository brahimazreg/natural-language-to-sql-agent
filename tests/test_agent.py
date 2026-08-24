from app.agent import run_agent


def test_run_agent():
    response = run_agent("Show me all students")

    assert response is not None
    assert len(response) == 25

