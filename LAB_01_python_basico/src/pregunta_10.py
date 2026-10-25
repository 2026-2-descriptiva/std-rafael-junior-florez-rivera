import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


# Recorre secuencialmente el archivo proyectando la cardinalidad de las columnas 4 y 5 por registro.
def pregunta_10() -> list[tuple[str, int, int]]:
    records: list[tuple[str, int, int]] = []
    with gzip.open(DATA_FILE, mode="rt", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                letter, _, _, codes, metrics = line.strip().split("\t")
                records.append((letter, len(codes.split(",")), len(metrics.split(","))))
    return records
