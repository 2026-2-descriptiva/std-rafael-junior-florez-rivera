from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"


# Genera la columna derivada mediante suma vectorizada con assign sin mutar la tabla base.
def pregunta_08() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE, sep="\t")
    return df.assign(suma=df["c0"] + df["c2"])
