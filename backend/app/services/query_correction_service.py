class QueryCorrectionService:

    def suggest_column_fix(self, wrong_column: str, schema: dict):
        closest_match = None

        for table, columns in schema.items():
            for col in columns:
                if wrong_column.lower() in col.lower() or col.lower() in wrong_column.lower():
                    closest_match = col
                    return closest_match

        return None

    def fix_query(self, query: str, wrong_column: str, correct_column: str):
        return query.replace(wrong_column, correct_column)
    
    def fix_group_by(self, query: str):
        if "count(" in query.lower() and "group by" not in query.lower():

            # extract column before COUNT
            parts = query.lower().split("select")[1].split("from")[0]
            columns = parts.split(",")

            non_agg = [
                col.strip()
                for col in columns
                if "count(" not in col
        ]

            if non_agg:
                group_col = non_agg[0]
                return query.strip().rstrip(";") + f" GROUP BY {group_col};"

        return None