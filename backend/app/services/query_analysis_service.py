import re

class QueryAnalysisService:
    def __init__(self):
        pass

    def analyze(self, query: str):
        query_clean = query.strip()
        query_lower = query_clean.lower()

        analysis = []

        select_info = self._extract_select(query_clean)
        if select_info:
            analysis.append(select_info)

        from_info = self._extract_from(query_clean)
        if from_info:
            analysis.append(from_info)

        join_info = self._extract_join(query_clean)
        if join_info:
            analysis.append(join_info)

        where_info = self._extract_where(query_clean)
        if where_info:
            analysis.append(where_info)

        group_by_info = self._extract_group_by(query_clean)
        if group_by_info:
            analysis.append(group_by_info)
        
        logical_issues = self.detect_logical_issues(query_clean)
        if logical_issues:
            for issue in logical_issues:
                analysis.append("⚠ Logical Issue: " + issue)

        join_issues = self.detect_join_issues(query_clean)
        if join_issues:
            for issue in join_issues:
                analysis.append("⚠ Logical Issue: " + issue)

        return analysis

    def _extract_select(self, query):
        match = re.search(r"select (.*?) from", query, re.IGNORECASE)
        if match:
            columns = match.group(1).strip()
            return f"You are selecting: {columns}."
        return None

    def _extract_from(self, query):
        match = re.search(r"from (.*?)( where| group by|$)", query, re.IGNORECASE)
        if match:
            table = match.group(1).strip()
            return f"You are querying from table: {table}."
        return None

    def _extract_where(self, query):
        match = re.search(r"where (.*?)( group by|$)", query, re.IGNORECASE)
        if match:
            condition = match.group(1).strip()
            return f"The WHERE clause filters rows where: {condition}."
        return None

    def _extract_group_by(self, query):
        match = re.search(r"group by (.*?)( order by|$)", query, re.IGNORECASE)
        if match:
            group_cols = match.group(1).strip()
            return f"The GROUP BY clause groups results by: {group_cols}."
        return None
    
    def _extract_join(self, query):
        match = re.search(r"join (.*?) on (.*?)( where| group by|$)", query, re.IGNORECASE)
        if match:
            table = match.group(1).strip()
            condition = match.group(2).strip()
            return f"You are joining with table: {table} using condition: {condition}."
        return None
    

    def detect_logical_issues(self, query: str):
        query_lower = query.lower()

        issues = []

        has_count = "count(" in query_lower
        has_group_by = "group by" in query_lower

        non_aggregate_columns = []

        # Detect aggregate without GROUP BY
        if has_count and not has_group_by:
            issues.append(
            "You are using an aggregate function (COUNT) without a GROUP BY clause."
            )

        # Detect selecting multiple columns with COUNT but no GROUP BY
        select_match = re.search(r"select (.*?) from", query, re.IGNORECASE)
        if select_match:
            columns = select_match.group(1)
            if "count(" in columns.lower():
                non_aggregate_columns = [
                col.strip()
                for col in columns.split(",")
                if "count(" not in col.lower()
                ]

            if non_aggregate_columns and not has_group_by:
                issues.append(
                    "You are selecting non-aggregated columns together with COUNT without GROUP BY."
                )

        return issues
    
    def detect_join_issues(self, query: str):
        query_lower = query.lower()
        issues = []

        if "join" in query_lower:
            if " on " not in query_lower:
                issues.append(
                    "JOIN detected but missing ON clause. JOIN requires a condition to relate tables."
            )

        return issues