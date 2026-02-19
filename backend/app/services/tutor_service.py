from app.services.query_analysis_service import QueryAnalysisService


class TutorService:
    def __init__(self):
        self.analysis_service = QueryAnalysisService()


    def generate_feedback(self, execution_result: dict, user_level: str = "beginner"):
        """
        execution_result: output from DatabaseService
        user_level: 'beginner' or 'advanced'
        """

        if execution_result["status"] == "success":
            return self._handle_success(execution_result, user_level)

        else:
            return self._handle_error(execution_result, user_level)

    def _handle_success(self, result, user_level):
        clause_explanations = self.analysis_service.analyze(result.get("original_query", ""))

        base_explanation = (
            "Your query executed successfully."
            if user_level == "beginner"
            else "Query executed successfully."
     )

        return {
            "status": "success",
            "data": result["data"],
            "explanation": base_explanation,
            "clause_analysis": clause_explanations
    }


    def _handle_error(self, result, user_level):
        error_type = result["error_type"]

        explanations = {
            "table_not_found": {
                "beginner": "The table name you used does not exist. Check spelling and capitalization.",
                "advanced": "The referenced table is not present in the current schema."
            },
            "column_not_found": {
                "beginner": "One of the columns does not exist in this table. Verify column names.",
                "advanced": "Column resolution failed. The specified attribute is undefined in this relation."
            },
            "syntax_error": {
                "beginner": "There is a syntax mistake in your SQL query. Review SQL keywords and structure.",
                "advanced": "The query violates SQL grammar rules."
            },
            "unsafe_query": {
                "beginner": "Only SELECT queries are allowed in this learning environment.",
                "advanced": "Data-modifying statements are restricted in the sandbox."
            },
            "unknown_error": {
                "beginner": "An unexpected error occurred.",
                "advanced": "Unhandled execution exception."
            }
        }

        explanation = explanations.get(error_type, explanations["unknown_error"])[user_level]

        return {
            "status": "error",
            "error_type": error_type,
            "message": result["message"],
            "explanation": explanation
        }
