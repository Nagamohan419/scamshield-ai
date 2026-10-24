
from pathlib import Path
import pandas as pd

# Get the root folder of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Excel dataset location
EXCEL_PATH = BASE_DIR / "data" / "ScamShield_Fraud_Dataset.xlsx"


def load_messages():
    """
    Load fraud and legitimate messages from Excel.
    """
    df = pd.read_excel(
        EXCEL_PATH,
        sheet_name="Messages"
    )

    return df


def load_keywords():
    """
    Load suspicious keywords from Excel.
    """
    df = pd.read_excel(
        EXCEL_PATH,
        sheet_name="Keywords"
    )

    return df


if __name__ == "__main__":

    print("\n========== SCAMSHIELD DATASET ==========\n")

    messages = load_messages()

    print("Total messages:", len(messages))

    print("\nColumn names:")
    print(messages.columns.tolist())

    print("\nFirst 5 messages:")
    print(messages.head().to_string(index=False))

    print("\n========== KEYWORDS ==========\n")

    keywords = load_keywords()

    print("Total keyword records:", len(keywords))

    print("\nKeyword column names:")
    print(keywords.columns.tolist())

    print("\nFirst 5 keyword records:")
    print(keywords.head().to_string(index=False))
