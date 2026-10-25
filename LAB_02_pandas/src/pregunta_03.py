from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"


# Contabiliza frecuencias con value_counts y ordena el indice para preservar orden alfabetico.
def pregunta_03() -> pd.Series:
    df = pd.read_csv(DATA_FILE, sep="\t")
    return df["c1"].value_counts().sort_index()
