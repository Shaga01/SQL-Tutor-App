from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.database_service import DatabaseService

app = FastAPI()
db_service = DatabaseService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "SQL Tutor backend is running"}

@app.post("/execute")
def execute_sql(request: QueryRequest):
    result = db_service.execute_query(request.query)
    return result
