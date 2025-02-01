# SATD (Self-Admitted Technical Debt) Commit Data Pipeline

This project is designed to **fetch, clean, and store** commit data from open-source repositories. It processes commit messages to remove unnecessary symbols, numbers, underscores, and formats timestamps. The cleaned data is then stored in both a **local PostgreSQL database** and a **Supabase PostgreSQL database**.

## **Project Structure**

```
📂 mozilla_satd_data_pipeline # Root directory of the project
├── fetch_commits.py         # Fetch commits from GitHub API
├── clean_data.py            # Clean commit messages and format data
├── save_data.py             # Save cleaned data to a local PostgreSQL database
├── save_to_supabase.py      # Save cleaned data to Supabase PostgreSQL
├── config.py                # Configuration settings for APIs and databases
├── commits.json             # Raw commit data (fetched)
├── cleaned_commits.json     # Cleaned commit data
├── cleaned_commits.csv      # Cleaned data in CSV format
├── README.md                # Project documentation
└── requirements.txt         # Dependencies
```

---

## **1. Setup Instructions**

### **Prerequisites**

Ensure you have the following installed on your system:

- Python 3.7+
- PostgreSQL
- GitHub API Access (if required)

### **Installation**

#### **Step 1: Clone the Repository**

```sh
git clone https://github.com/your-repo/satd_commit_pipeline.git
cd satd_commit_pipeline
```

#### **Step 2: Create and Activate a Virtual Environment**

```sh
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

#### **Step 3: Install Dependencies**

```sh
pip install -r requirements.txt
```

#### **Step 4: Configure the Project**

Edit `config.py` to set up your **GitHub API URL**, **headers**, and **database connection settings**.

Example `config.py`:

```python
GITHUB_API_URL = "https://api.github.com/repos/mozilla/gecko-dev/commits"
HEADERS = {"Authorization": "token YOUR_GITHUB_TOKEN"}

DB_CONFIG = {
    "dbname": "your_local_db",
    "user": "your_db_user",
    "password": "your_db_password",
    "host": "localhost",
    "port": "5432"
}
```

For **Supabase configuration**, update `save_to_supabase.py` with your **Supabase credentials**.

---

## **2. Running the Pipeline**

### **Step 1: Fetch Commits from GitHub**

```sh
python fetch_commits.py
```

- This script fetches commits from GitHub and saves them to `commits.json`.
- The default time range is from **2020-01-01 to 2025-01-01**.

### **Step 2: Clean the Data**

```sh
python clean_data.py
```

- Removes **symbols**, **numbers**, **underscores**, and extra spaces.
- Converts timestamps to a readable format.
- Saves the cleaned data in `cleaned_commits.json` and `cleaned_commits.csv`.

### **Step 3: Save to Local PostgreSQL**

```sh
python save_data.py
```

- Creates `stad_schema.commits` table (if it doesn’t exist).
- Inserts cleaned data into the **local PostgreSQL database**.

### **Step 4: Save to Supabase PostgreSQL**

```sh
python save_to_supabase.py
```

- Creates `stad_schema.commits` table in **Supabase**.
- Inserts cleaned data into the **Supabase PostgreSQL database**.

---

## **3. Database Schema**

The table `stad_schema.commits` contains:

| Column  | Type               | Description            |
| ------- | ------------------ | ---------------------- |
| id(sha)      | SERIAL PRIMARY KEY | Auto-incremented ID    |
| author  | TEXT               | Commit author name     |
| date    | TIMESTAMP          | Formatted commit date  |
| message | TEXT               | Cleaned commit message |

---

## **4. Troubleshooting**

### **Issue: Fetching Only 100 Commits**

- **Solution**: GitHub API **pagination** limits results to 100 per request.
- Update `fetch_commits.py` to fetch multiple pages:

```python
params = {"since": since, "until": until, "per_page": 100, "page": 1}
while True:
    response = requests.get(GITHUB_API_URL, headers=HEADERS, params=params)
    data = response.json()
    if not data:
        break
    commits.extend(data)
    params["page"] += 1
```

### **Issue: Database Connection Error**

- Check that **PostgreSQL is running**.
- Ensure correct **database credentials** in `config.py`.
- For **Supabase**, verify your **password and host settings**.

### **Issue: Data Not Showing in Supabase**

- Run `python save_to_supabase.py` again.
- Check if `stad_schema.commits` exists in Supabase.
- Log into Supabase and run:

```sql
SELECT * FROM stad_schema.commits;
```

---

## **5. Future Enhancements**

- Add a **Docker setup** for easy deployment.
- Implement **real-time streaming** using Kafka or WebSockets.
- Build a **dashboard** to visualize commit trends.

---

## **6. License**

This project is licensed under the **MIT License**.

---

## **7. Contact**

For any issues, reach out to:
📧 **Email**: [ishmaelloabtkb19@gmail.com](mailto\:ishmaelloabtkb19@gmail.com)\
🔗 **LinkedIn**: [Ishmael Kabu Abayateye](http://www.linkedin.com/in/ikabayateye)



