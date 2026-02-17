import sqlite3

class DatabaseService:
    def __init__(self):
        # In-memory database (resets every restart)
        self.connection = sqlite3.connect(":memory:", check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self._initialize_database()

    def _initialize_database(self):
        cursor = self.connection.cursor()

        # Create a sample table
        cursor.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                grade TEXT
            );
        """)

        # Insert sample data
        cursor.executemany("""
            INSERT INTO students (name, age, grade)
            VALUES (?, ?, ?)
        """, [
            ("Alice", 20, "A"),
            ("Bob", 22, "B"),
            ("Charlie", 21, "A"),
        ])

        self.connection.commit()

    def execute_query(self, query: str):
        cursor = self.connection.cursor()

        try:
            cursor.execute(query)

            if query.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            else:
                self.connection.commit()
                return {"message": "Query executed successfully"}

        except Exception as e:
            return {"error": str(e)}
