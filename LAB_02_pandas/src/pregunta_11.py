from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "tbl1.tsv"


# Ordena globalmente por clave y letra antes de agrupar para evitar ordenamientos fila por fila.
def pregunta_11() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE, sep="\t")
    return df.sort_values(["c0", "c4"]).groupby("c0", as_index=False)["c4"].agg(",".join)
