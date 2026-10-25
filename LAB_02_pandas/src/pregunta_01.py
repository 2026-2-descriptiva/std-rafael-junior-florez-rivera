from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"


# Obtiene el conteo de registros directamente desde shape[0] sin recorrer filas.
def pregunta_01() -> int:
    df = pd.read_csv(DATA_FILE, sep="\t")
    return df.shape[0]
