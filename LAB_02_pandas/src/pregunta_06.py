from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "tbl1.tsv"


# Normaliza cadenas a mayusculas de forma vectorizada antes de deduplicar y ordenar.
def pregunta_06() -> list[str]:
    df = pd.read_csv(DATA_FILE, sep="\t")
    return sorted(df["c4"].str.upper().unique().tolist())
