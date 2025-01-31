# main.py

from fetch_commits import fetch_commits
from clean_data import clean_data
from save_data import save_to_csv, save_to_postgres
import json

def main():
    # Fetch commits
    print("Fetching commits...")
    commits = fetch_commits("2020-01-01T00:00:00Z", "2025-01-01T00:00:00Z")
    with open("commits.json", "w") as f:
        json.dump(commits, f, indent=4)
    print("Commits saved to commits.json")
    
    # Clean commits
    print("Cleaning data...")
    cleaned_commits = clean_data(commits)
    with open("cleaned_commits.json", "w") as f:
        json.dump(cleaned_commits, f, indent=4)
    print("Cleaned data saved to cleaned_commits.json")
    
    # Save cleaned data
    print("Saving data...")
    save_to_csv(cleaned_commits, "cleaned_commits.csv")
    save_to_postgres(cleaned_commits)
    print("Process completed successfully!")

if __name__ == "__main__":
    main()
