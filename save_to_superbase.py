import json
import psycopg2

# Supabase database configuration
SUPABASE_DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "DO YOU KNOW ME",
    "host": "db.jgdzrkkfyvvoqemuezas.supabase.co",
    "port": "5432"
}

def load_cleaned_commits(file_path):
    """Load cleaned commit data from a JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)

def save_to_supabase(cleaned_commits):
    """Save cleaned commit data to Supabase PostgreSQL database."""
    try:
        # Connect to Supabase PostgreSQL
        conn = psycopg2.connect(**SUPABASE_DB_CONFIG)
        cursor = conn.cursor()

        # Create schema if it does not exist
        cursor.execute("CREATE SCHEMA IF NOT EXISTS stad_schema;")
        
        # Create commits table inside stad_schema in Supabase
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stad_schema.commits (
                id SERIAL PRIMARY KEY,  -- Auto-incrementing ID
                author TEXT,
                date TIMESTAMP,
                message TEXT
            )
        ''')
        
        # Insert cleaned data into the Supabase PostgreSQL table
        for commit in cleaned_commits:
            cursor.execute('''
                INSERT INTO stad_schema.commits (author, date, message)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            ''', (commit["author"], commit["date"], commit["message"]))

        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()

        print("Data successfully saved to Supabase PostgreSQL database.")
    
    except Exception as e:
        print(f"Error saving to Supabase: {e}")

if __name__ == "__main__":
    # Load cleaned commit data
    cleaned_commits = load_cleaned_commits("cleaned_commits.json")
    
    # Save data to Supabase PostgreSQL
    save_to_supabase(cleaned_commits)
