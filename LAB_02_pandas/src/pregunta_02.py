from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"


# Extrae la cardinalidad de columnas desde shape[1] sobre el esquema cargado.
def pregunta_02() -> int:
    df = pd.read_csv(DATA_FILE, sep="\t")
    return df.shape[1]
