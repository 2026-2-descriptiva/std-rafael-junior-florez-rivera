from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"


# Extrae los cuatro primeros caracteres ISO como texto para tolerar fechas no bisiestas invalidas.
def pregunta_09() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE, sep="\t")
    return df.assign(year=df["c3"].str.slice(0, 4))
