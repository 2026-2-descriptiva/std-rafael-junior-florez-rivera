from collections import Counter
import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


# Extrae el mes como subcadena ISO (MM) para preservar el cero inicial y el orden lexicografico.
def pregunta_04() -> list[tuple[str, int]]:
    with gzip.open(DATA_FILE, mode="rt", encoding="utf-8") as file:
        months = Counter(line.split("\t")[2][5:7] for line in file if line.strip())
    return sorted(months.items())
