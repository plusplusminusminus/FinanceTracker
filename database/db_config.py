import sqlite3

class Database:
    def __init__(self, filename="finance_tracker.db"):
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()

        # Create the users table
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )
                ''')

        # Create the transactions table
        self.cursor.execute('''
                   CREATE TABLE IF NOT EXISTS transactions (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       TransactionDate DATE NOT NULL,
                       amount FLOAT NOT NULL
                   )
               ''')

        # Insert a sample user for testing
        self.cursor.execute("""
            INSERT INTO users (username, password) 
            VALUES ('student', '12345')
        """)

        self.conn.commit()

    def query_user(self, username, password):
        self.cursor.execute("""
            SELECT * FROM users 
            WHERE username = ? AND password = ?
        """, (username, password))

        return self.cursor.fetchall()

    def insert_transactions_into_db(self, df):
        df.to_sql("transactions", self.conn, if_exists="append", index=False)

    def close(self):
        self.conn.close()