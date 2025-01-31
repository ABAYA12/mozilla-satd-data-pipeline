import requests
import json
from config import GITHUB_API_URL, HEADERS

def fetch_commits(since, until):
    commits = []
    page = 1  # Start from the first page
    while True:
        params = {
            "since": since,
            "until": until,
            "per_page": 1000,  # Max per page
            "page": page  # Paginate through pages
        }
        response = requests.get(GITHUB_API_URL, headers=HEADERS, params=params)
        
        if response.status_code == 200:
            page_commits = response.json()
            if not page_commits:  # If no commits are returned, break the loop
                break
            commits.extend(page_commits)
            page += 1  # Move to the next page
        else:
            print(f"Error fetching data: {response.status_code}, {response.text}")
            break

    return commits

if __name__ == "__main__":
    commits = fetch_commits("2020-01-01T00:00:00Z", "2025-01-01T00:00:00Z")
    with open("commits.json", "w") as f:
        json.dump(commits, f, indent=4)
    print(f"Commits saved to commits.json, Total: {len(commits)} commits")
