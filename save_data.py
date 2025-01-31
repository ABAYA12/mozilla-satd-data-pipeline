import json
import pandas as pd
import psycopg2
from config import DB_CONFIG

def load_cleaned_commits(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def save_to_csv(cleaned_commits, file_path):
    df = pd.DataFrame(cleaned_commits)
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

def save_to_postgres(cleaned_commits):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Create the schema if it doesn't exist
    cursor.execute("CREATE SCHEMA IF NOT EXISTS stad_schema;")
    
    # Create the commits table in the stad_schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stad_schema.commits (
            sha TEXT PRIMARY KEY,
            author TEXT,
            date TIMESTAMP,
            message TEXT
        )
    ''')
    
    # Insert cleaned data into the PostgreSQL table
    for commit in cleaned_commits:
        cursor.execute('''
            INSERT INTO stad_schema.commits (sha, author, date, message)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (sha) DO NOTHING
        ''', (commit["sha"], commit["author"], commit["date"], commit["message"]))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Data saved to PostgreSQL database")

if __name__ == "__main__":
    cleaned_commits = load_cleaned_commits("cleaned_commits.json")
    save_to_csv(cleaned_commits, "cleaned_commits.csv")
    save_to_postgres(cleaned_commits)
