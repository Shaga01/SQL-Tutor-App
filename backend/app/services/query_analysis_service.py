class QueryAnalysisService:
    def __init__(self):
        pass

    def analyze(self, query: str):
        query_lower = query.lower()

        analysis = []

        if "select" in query_lower:
            analysis.append(self._analyze_select(query))

        if "from" in query_lower:
            analysis.append(self._analyze_from(query))

        if "where" in query_lower:
            analysis.append(self._analyze_where(query))

        if "group by" in query_lower:
            analysis.append(self._analyze_group_by(query))

        if "join" in query_lower:
            analysis.append(self._analyze_join(query))

        return analysis

    def _analyze_select(self, query):
        return "SELECT clause specifies which columns are retrieved."

    def _analyze_from(self, query):
        return "FROM clause specifies the table being queried."

    def _analyze_where(self, query):
        return "WHERE clause filters rows based on conditions."

    def _analyze_group_by(self, query):
        return "GROUP BY groups rows for aggregation functions like COUNT or AVG."

    def _analyze_join(self, query):
        return "JOIN combines rows from multiple tables based on a related column."
