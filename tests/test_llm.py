from app.llm import generate_sql


def test_generate_sql():
    response = generate_sql(
        "How many students are enrolled in each program?"
    )

    assert response is not None
    assert "SELECT" in response.upper()
    assert "students" in response.lower()