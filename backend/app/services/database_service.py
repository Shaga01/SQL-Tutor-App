import sqlite3

class DatabaseService:
    def __init__(self):
        # In-memory database (resets every restart)
        self.connection = sqlite3.connect(":memory:", check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self._initialize_database()

    def _initialize_database(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            major_id INTEGER
            );
        """)

        cursor.execute("""
            CREATE TABLE majors (
            id INTEGER PRIMARY KEY,
            major_name TEXT
        );
        """)

        cursor.executemany("""
            INSERT INTO majors (major_name)
            VALUES (?)
        """, [
            ("Computer Science",),
            ("Mathematics",),
            ("Physics",)
        ])

        cursor.executemany("""
            INSERT INTO students (name, age, major_id)
            VALUES (?, ?, ?)
        """, [
            ("Alice", 20, 1),
            ("Bob", 22, 2),
            ("Charlie", 21, 1),
        ])

        self.connection.commit()

    def execute_query(self, query: str):
        if not self._is_query_safe(query):
            return {
            "status": "error",
            "error_type": "unsafe_query",
            "message": "Only SELECT queries are allowed in this tutor."
        }

        cursor = self.connection.cursor()

        try:
            cursor.execute(query)

            rows = cursor.fetchall()

            return {
                "status": "success",
                "data": [dict(row) for row in rows]
            }

        except Exception as e:
            return self._classify_error(str(e))

        
    def _is_query_safe(self, query: str) -> bool:
        forbidden_keywords = ["drop", "delete", "update", "insert", "alter"]

        query_lower = query.lower()
        for keyword in forbidden_keywords:
            if keyword in query_lower:
                return False

        return True
    

    def _classify_error(self, error_message: str):
        error_message_lower = error_message.lower()

        if "no such table" in error_message_lower:
            return {
            "status": "error",
            "error_type": "table_not_found",
            "message": "The table you referenced does not exist."
        }

        elif "no such column" in error_message_lower:
            return {
            "status": "error",
            "error_type": "column_not_found",
            "message": "One of the columns you used does not exist in the table."
        }

        elif "syntax error" in error_message_lower:
            return {
            "status": "error",
            "error_type": "syntax_error",
            "message": "There is a SQL syntax error in your query."
        }

        else:
            return {
            "status": "error",
            "error_type": "unknown_error",
            "message": error_message
        }

    def get_schema_info(self):
        cursor = self.connection.cursor()

        schema = {}

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            schema[table_name] = [col[1] for col in columns]

        return schema


