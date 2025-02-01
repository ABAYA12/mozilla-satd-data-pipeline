# clean.py

import pandas as pd
import re
from config import FILE_PATHS

def clean_data():
    # Load uncleaned data
    df = pd.read_csv(FILE_PATHS["uncleaned_data"])

    # Clean text fields
    def clean_text(text):
        if isinstance(text, str):
            text = re.sub(r"[_,;'/\\\|{}[\]!@#%^&*()=+]", " ", text)
            text = " ".join(text.split())
            text = text.lower()
        return text

    # Apply cleaning to text fields
    df["Product Name"] = df["Product Name"].apply(clean_text)
    df["Category"] = df["Category"].apply(clean_text)
    df["Customer Location"] = df["Customer Location"].apply(clean_text)

    # Format Purchase Date
    df["Purchase Date"] = pd.to_datetime(df["Purchase Date"]).dt.strftime("%Y-%m-%d %H:%M:%S")

    # Save cleaned data to CSV
    df.to_csv(FILE_PATHS["cleaned_data"], index=False)
    print("Data cleaned and saved to:", FILE_PATHS["cleaned_data"])

if __name__ == "__main__":
    clean_data()