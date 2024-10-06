from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_db_query import query_database

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query(request: QueryRequest):
    answer = query_database(request.question)
    if not answer:
        raise HTTPException(status_code=400, detail="Unable to generate a valid SQL query.")
    return {"answer": answer}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)