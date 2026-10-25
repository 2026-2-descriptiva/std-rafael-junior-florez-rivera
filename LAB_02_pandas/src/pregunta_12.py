from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "tbl2.tsv"


# Construye el par clave:valor de forma vectorizada tras ordenar por c5a y colapsa por registro c0.
def pregunta_12() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE, sep="\t").sort_values(["c0", "c5a"])
    df = df.assign(c5=df["c5a"] + ":" + df["c5b"].astype(str))
    return df.groupby("c0", as_index=False)["c5"].agg(",".join)
