from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


# Cruza las tablas por llave primaria c0 proyectando solo columnas utiles antes de sumar por c1.
def pregunta_13() -> pd.Series:
    tbl0 = pd.read_csv(DATA_DIR / "tbl0.tsv", sep="\t", usecols=["c0", "c1"])
    tbl2 = pd.read_csv(DATA_DIR / "tbl2.tsv", sep="\t", usecols=["c0", "c5b"])
    merged = pd.merge(tbl0, tbl2, on="c0")
    return merged.groupby("c1")["c5b"].sum()
