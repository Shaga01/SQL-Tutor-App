from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.database_service import DatabaseService
from app.services.tutor_service import TutorService


app = FastAPI()
db_service = DatabaseService()
tutor_service = TutorService()


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
    execution_result = db_service.execute_query(request.query)

    execution_result["original_query"] = request.query

    tutor_response = tutor_service.generate_feedback(
        execution_result,
        user_level="beginner"
    )

    return tutor_response


