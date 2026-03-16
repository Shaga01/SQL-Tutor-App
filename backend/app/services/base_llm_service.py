class BaseLLMService:
    def generate_sql(self, natural_language_query: str, schema: dict) -> str:
        raise NotImplementedError