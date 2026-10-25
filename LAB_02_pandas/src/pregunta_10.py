from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"


# Ordena numericamente c2 antes de castear a texto para conservar orden creciente al concatenar.
def pregunta_10() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE, sep="\t")
    ordered = df.sort_values(["c1", "c2"]).assign(c2=lambda d: d["c2"].astype(str))
    return ordered.groupby("c1")[["c2"]].agg(":".join)
