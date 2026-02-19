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

        where_info = self._extract_where(query_clean)
        if where_info:
            analysis.append(where_info)

        group_by_info = self._extract_group_by(query_clean)
        if group_by_info:
            analysis.append(group_by_info)

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