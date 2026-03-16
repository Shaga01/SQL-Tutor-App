import requests
from app.services.base_llm_service import BaseLLMService

class SQLCoderService(BaseLLMService):

    def generate_sql(self, natural_language_query: str, schema: dict) -> str:
        schema_text = self._format_schema(schema)

        prompt = f"""
You are an expert SQL generator.

Database schema:
{schema_text}

Task:
Write a valid SQLite SELECT query for the following request.

Request:
{natural_language_query}

SQL Query:
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "sqlcoder",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()
        sql = result["response"].strip()

        return self._clean_sql(sql)

    def _format_schema(self, schema: dict):
        text = ""
        for table, columns in schema.items():
            text += f"{table}({', '.join(columns)})\n"
        return text

    def _clean_sql(self, sql: str):
    # Remove markdown
        sql = sql.replace("```sql", "").replace("```", "")

    # Remove common model tokens
        sql = sql.replace("<s>", "").replace("</s>", "")

    # Keep only SELECT statement
        if "SELECT" in sql.upper():
            sql = sql[sql.upper().index("SELECT"):]

        return sql.strip()