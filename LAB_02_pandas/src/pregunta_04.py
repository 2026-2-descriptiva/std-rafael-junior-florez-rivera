from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"


# Calcula la media aritmetica por categoria mediante agregacion vectorizada sobre c1.
def pregunta_04() -> pd.Series:
    df = pd.read_csv(DATA_FILE, sep="\t")
    return df.groupby("c1")["c2"].mean()
