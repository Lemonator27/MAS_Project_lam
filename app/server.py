import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel

ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(ROOT, os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from orchestration.mas_graph import app as mas_app


class Query(BaseModel):
    query: str


app = FastAPI(title="MAS Finance API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query")
def run_query(payload: Query):
    result = mas_app.invoke({"messages": [{"role": "user", "content": payload.query}]})
    # result contains state with 'result'
    return {"result": result.get("result")}
