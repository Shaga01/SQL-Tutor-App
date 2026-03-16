#Capstone Project-Shashwat Gautam
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.database_service import DatabaseService
from app.services.tutor_service import TutorService
from app.services.sqlcoder_service import SQLCoderService

app = FastAPI()
db_service = DatabaseService()
tutor_service = TutorService()
llm_service = SQLCoderService()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class NLRequest(BaseModel):
    question: str



@app.get("/")
def root():
    return {"message": "SQL Tutor backend is running"}

@app.post("/execute")
def execute_sql(request: QueryRequest):
    execution_result = db_service.execute_query(request.query)
    execution_result["original_query"] = request.query

    schema_info = db_service.get_schema_info()

    tutor_response = tutor_service.generate_feedback(
        execution_result,
        user_level="beginner",
        schema=schema_info
    )

    return tutor_response



@app.post("/generate-sql")
def generate_sql(request: NLRequest):
    schema_info = db_service.get_schema_info()

    generated_sql = llm_service.generate_sql(
        request.question,
        schema_info
    )

    execution_result = db_service.execute_query(generated_sql)
    execution_result["original_query"] = generated_sql

    tutor_response = tutor_service.generate_feedback(
        execution_result,
        user_level="beginner",
        schema=schema_info
    )

    return {
        "generated_sql": generated_sql,
        "tutor_response": tutor_response
    }


