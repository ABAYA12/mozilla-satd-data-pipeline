import json
import re
from datetime import datetime

def load_commits(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def clean_commit_message(message):
    # Strip extra spaces
    message = message.strip()
    # Remove all non-alphanumeric characters (excluding spaces and basic punctuation)
    message = re.sub(r'[^\w\s]', '', message)
    # Remove numbers
    message = re.sub(r'\d+', '', message)
    # Remove underscores
    message = message.replace('_', ' ')
    # Replace multiple spaces with a single space
    message = re.sub(r'\s+', ' ', message)
    return message

def format_date(date_str):
    try:
        # Parse the date from ISO 8601 format
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        # Format the date in a more readable format
        return date_obj.strftime("%B %d, %Y %I:%M %p")  # Example: 'December 29, 2024 07:02 AM'
    except ValueError:
        # Return the original date if parsing fails
        return date_str

def clean_data(commits):
    cleaned_commits = []
    sha_counter = 1  # Start the auto-increment counter for SHA

    for commit in commits:
        cleaned_commit = {
            "sha": sha_counter,  # Assign the auto-incremented SHA value
            "author": commit.get("commit", {}).get("author", {}).get("name", "Unknown"),
            "date": format_date(commit.get("commit", {}).get("author", {}).get("date", "")),
            "message": clean_commit_message(commit.get("commit", {}).get("message", ""))
        }
        cleaned_commits.append(cleaned_commit)
        sha_counter += 1  # Increment the SHA counter for the next commit

    return cleaned_commits

if __name__ == "__main__":
    commits = load_commits("commits.json")
    cleaned_commits = clean_data(commits)
    
    with open("cleaned_commits.json", "w") as f:
        json.dump(cleaned_commits, f, indent=4)
    
    print("Cleaned data saved to cleaned_commits.json")
