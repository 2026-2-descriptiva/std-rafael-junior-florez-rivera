from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "solicitudes_de_credito.csv.gz"
OUTPUT_FILE = BASE_DIR / "submission" / "solicitudes_de_credito.csv"

COLUMNS = [
    "sexo",
    "tipo_de_emprendimiento",
    "idea_negocio",
    "barrio",
    "estrato",
    "comuna_ciudadano",
    "fecha_de_beneficio",
    "monto_del_credito",
    "línea_credito",
]
TEXT_COLUMNS = [
    "sexo",
    "tipo_de_emprendimiento",
    "idea_negocio",
    "barrio",
    "línea_credito",
]


# Unifica formatos heterogeneos de fecha probando en cascada dia-primero y ano-primero sin perder registros.
def _normalize_dates(series: pd.Series) -> pd.Series:
    parsed = pd.to_datetime(series, format="%d/%m/%Y", errors="coerce")
    for fmt in ("%Y/%m/%d", "%Y-%m-%d"):
        parsed = parsed.fillna(pd.to_datetime(series, format=fmt, errors="coerce"))
    return parsed.dt.strftime("%Y-%m-%d")


# Estandariza texto, montos y fechas preservando nulos legitimos en comuna_ciudadano antes de deduplicar.
def pregunta_01() -> None:
    df = pd.read_csv(DATA_FILE, sep=";", index_col=0)[COLUMNS]
    required_cols = [col for col in COLUMNS if col != "comuna_ciudadano"]
    df = df.dropna(subset=required_cols).copy()

    for col in TEXT_COLUMNS:
        df[col] = (
            df[col]
            .astype(str)
            .str.lower()
            .str.replace("_", " ", regex=False)
            .str.replace("-", " ", regex=False)
            .str.strip()
        )

    df["estrato"] = df["estrato"].astype(int)
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(float).astype("Int64")
    df["fecha_de_beneficio"] = _normalize_dates(df["fecha_de_beneficio"])
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .astype(float)
        .astype(int)
    )

    df = df.drop_duplicates()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, sep=";", index=False, encoding="utf-8")
