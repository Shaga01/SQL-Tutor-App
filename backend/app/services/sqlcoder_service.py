import requests
import re
from app.services.base_llm_service import BaseLLMService

class SQLCoderService(BaseLLMService):

    def generate_sql(self, natural_language_query: str, schema: dict) -> str:
        schema_text = self._format_schema(schema)

        prompt = f"""
        ### Instructions:
        You are a SQLite expert. Generate ONLY a SQL SELECT query.

        ### Database Schema:
        {schema_text}

        ### Question:
        {natural_language_query}

        ### SQL:
        """

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
        "model": "sqlcoder",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "top_p": 0.1,
            "num_predict": 200
            }
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

    # remove markdown and tokens
        sql = sql.replace("```sql", "").replace("```", "")
        sql = sql.replace("<s>", "").replace("</s>", "")

    # remove comments or weird text
        sql = sql.replace("#", "")

    # try extracting SELECT query
        match = re.search(r"(SELECT\s+.*?;)", sql, re.IGNORECASE | re.DOTALL)

        if match:
            return match.group(1).strip()

    # fallback: try if SELECT exists without semicolon
        match = re.search(r"(SELECT\s+.*)", sql, re.IGNORECASE | re.DOTALL)

        if match:
            return match.group(1).strip() + ";"

        return sql.strip()