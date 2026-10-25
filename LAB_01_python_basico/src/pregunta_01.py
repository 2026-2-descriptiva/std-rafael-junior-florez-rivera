import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


# Procesa el archivo en streaming con un generador para sumar la columna 2 en memoria constante.
def pregunta_01() -> int:
    with gzip.open(DATA_FILE, mode="rt", encoding="utf-8") as file:
        return sum(int(line.split("\t")[1]) for line in file if line.strip())
