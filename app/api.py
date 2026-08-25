from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent import run_agent

app = FastAPI()


class QuestionRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/home")
def home():
    return {"message": "Natural Language to SQL project"}


@app.post("/query")
def query(request: QuestionRequest):
    try:
        response = run_agent(request.query)
        return {"answer": response}

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )