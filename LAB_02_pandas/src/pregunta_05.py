from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"


# Determina el valor maximo de c2 por categoria usando reduccion vectorizada.
def pregunta_05() -> pd.Series:
    df = pd.read_csv(DATA_FILE, sep="\t")
    return df.groupby("c1")["c2"].max()
