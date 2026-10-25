import json
from pathlib import Path
import re
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "ventas.csv.gz"
REPORT_FILE = BASE_DIR / "submission" / "data_quality_report.json"

REQUIRED_COLUMNS = (
    "supplier_id",
    "supplier",
    "country",
    "city",
    "purchase_date",
    "amount",
    "discount",
    "weight",
    "units",
    "unit_price",
    "contact_email",
)
MISSING_TOKENS = {"", "N/A"}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# Valida si un texto numerico representa un entero estrictamente positivo sin fallar ante formatos sucios.
def _is_positive_integer(raw_value: str) -> bool:
    try:
        numeric = float(raw_value)
        return numeric > 0 and numeric.is_integer()
    except ValueError:
        return False


# Audita el archivo crudo sin mutar celdas para evidenciar anomalias estructurales y de dominio en JSON.
def main() -> dict:
    df = pd.read_csv(DATA_FILE, encoding="utf-8-sig", dtype=str, keep_default_na=False)
    df.columns = [
        re.sub(r"\s+", "_", col.lstrip("\ufeff").strip().lower()) for col in df.columns
    ]

    present = set(df.columns)
    required = set(REQUIRED_COLUMNS)

    non_missing_emails = df.loc[~df["contact_email"].isin(MISSING_TOKENS), "contact_email"]
    non_missing_units = df.loc[~df["units"].isin(MISSING_TOKENS), "units"]

    report = {
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "missing_required_columns": sorted(required - present),
        "unexpected_columns": sorted(present - required),
        "duplicate_row_count": int(df.duplicated().sum()),
        "duplicate_supplier_id_row_count": int(df["supplier_id"].duplicated(keep=False).sum()),
        "missing_value_count_by_column": {
            col: int(df[col].isin(MISSING_TOKENS).sum()) for col in df.columns
        },
        "invalid_email_count": int((~non_missing_emails.str.match(EMAIL_PATTERN)).sum()),
        "invalid_unit_count": int((~non_missing_units.map(_is_positive_integer)).sum()),
        "country_values": sorted(df["country"].unique().tolist()),
    }

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report
