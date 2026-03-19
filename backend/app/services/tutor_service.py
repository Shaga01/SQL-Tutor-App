import re
from app.services.query_analysis_service import QueryAnalysisService
from app.services.query_correction_service import QueryCorrectionService


class TutorService:
    def __init__(self):
        self.analysis_service = QueryAnalysisService()
        self.correction_service = QueryCorrectionService()

    def generate_feedback(self, execution_result: dict, user_level: str = "beginner", schema: dict = None):
        """
        execution_result: output from DatabaseService
        user_level: 'beginner' or 'advanced'
        """

        if execution_result["status"] == "success":
            return self._handle_success(execution_result, user_level, schema)
        else:
            return self._handle_error(execution_result, user_level, schema)

    def _handle_success(self, result, user_level, schema=None):
        clause_explanations = self.analysis_service.analyze(
            result.get("original_query", ""),
            schema
        )

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

    def _handle_error(self, result, user_level, schema=None):
        error_type = result["error_type"]

        # ✅ Fixed column_not_found handling
        if error_type == "column_not_found":

            wrong_column = None
            match = re.search(r"no such column: (\w+)", result["message"])

            if match:
                wrong_column = match.group(1)

            suggested_column = None
            corrected_query = None

            if wrong_column and schema:
                suggested_column = self.correction_service.suggest_column_fix(
                    wrong_column,
                    schema
                )

            if suggested_column:
                corrected_query = self.correction_service.fix_query(
                    result.get("original_query", ""),
                    wrong_column,
                    suggested_column
                )

            return {
                "status": "error",
                "error_type": error_type,
                "message": result["message"],
                "explanation": f"Column '{wrong_column}' does not exist.",
                "suggestion": f"Did you mean '{suggested_column}'?" if suggested_column else None,
                "corrected_query": corrected_query
            }

        # Dictionary-based handling for all other errors
        explanations = {
            "table_not_found": {
                "beginner": "The table name you used does not exist. Check spelling and capitalization.",
                "advanced": "The referenced table is not present in the current schema."
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

        explanation = explanations.get(
            error_type, explanations["unknown_error"]
        )[user_level]

        return {
            "status": "error",
            "error_type": error_type,
            "message": result["message"],
            "explanation": explanation
        }