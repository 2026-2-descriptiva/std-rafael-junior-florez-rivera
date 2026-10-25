from collections import Counter
import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


# Usa Counter para contabilizar frecuencias en una sola pasada y retorna tuplas ordenadas por clave.
def pregunta_02() -> list[tuple[str, int]]:
    with gzip.open(DATA_FILE, mode="rt", encoding="utf-8") as file:
        counts = Counter(line.split("\t")[0] for line in file if line.strip())
    return sorted(counts.items())
