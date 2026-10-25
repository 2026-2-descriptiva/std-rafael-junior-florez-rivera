from pathlib import Path
import re
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SUBMISSION_DIR = BASE_DIR / "submission"

MONTH_MAP = {
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12",
}


# Descompone el dataset bancario particionado en entidades normalizadas cliente, campana y economia.
def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    files = sorted(
        DATA_DIR.glob("bank-marketing-campaing-*.csv.gz"),
        key=lambda p: int(re.search(r"\d+", p.name).group()),
    )
    raw_df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

    client = pd.DataFrame(
        {
            "client_id": raw_df["client_id"],
            "age": raw_df["age"],
            "job": (
                raw_df["job"]
                .str.replace(".", "", regex=False)
                .str.replace("-", "_", regex=False)
            ),
            "marital": raw_df["marital"],
            "education": (
                raw_df["education"]
                .str.replace(".", "_", regex=False)
                .replace("unknown", pd.NA)
            ),
            "credit_default": (raw_df["credit_default"] == "yes").astype(int),
            "mortgage": (raw_df["mortgage"] == "yes").astype(int),
        }
    )

    last_contact_date = (
        "2022-"
        + raw_df["month"].str.lower().map(MONTH_MAP)
        + "-"
        + raw_df["day"].astype(str).str.zfill(2)
    )
    campaign = pd.DataFrame(
        {
            "client_id": raw_df["client_id"],
            "number_contacts": raw_df["number_contacts"],
            "contact_duration": raw_df["contact_duration"],
            "previous_campaign_contacts": raw_df["previous_campaign_contacts"],
            "previous_outcome": (raw_df["previous_outcome"] == "success").astype(int),
            "campaign_outcome": (raw_df["campaign_outcome"] == "yes").astype(int),
            "last_contact_date": last_contact_date,
        }
    )

    economics = pd.DataFrame(
        {
            "client_id": raw_df["client_id"],
            "cons_price_idx": raw_df["cons_price_idx"],
            "euribor_three_months": raw_df["euribor_three_months"],
        }
    )

    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    client.to_csv(SUBMISSION_DIR / "client.csv", index=False)
    campaign.to_csv(SUBMISSION_DIR / "campaign.csv", index=False)
    economics.to_csv(SUBMISSION_DIR / "economics.csv", index=False)

    return client, campaign, economics
