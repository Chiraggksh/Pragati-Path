import sqlite3

# Path to your existing SQLite .db file
db_path = 'civic_issues.db'  # <-- Replace this with your actual file path

# SQL statement to create the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS issue_validations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue_id TEXT REFERENCES issues(id),
    image_valid BOOLEAN,
    image_msg TEXT,
    florence_caption TEXT,
    civic_score TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def create_table(db_path, create_sql):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute the SQL to create the table
        cursor.execute(create_sql)
        
        # Commit changes and close the connection
        conn.commit()
        conn.close()
        
        print("Table 'issue_validations' created successfully (if it didn't already exist).")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

# Run the function
create_table(db_path, create_table_sql)
