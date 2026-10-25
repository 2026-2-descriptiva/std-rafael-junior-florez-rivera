from collections import defaultdict
import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


# Acumula sumas por categoria con defaultdict(int) para evitar verificaciones manuales de claves.
def pregunta_03() -> list[tuple[str, int]]:
    totals: dict[str, int] = defaultdict(int)
    with gzip.open(DATA_FILE, mode="rt", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                letter, value, *_ = line.split("\t")
                totals[letter] += int(value)
    return sorted(totals.items())
