from collections import defaultdict
import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


# Suma los enteros de los pares clave:valor por registro y los acumula segun la letra de la columna 1.
def pregunta_12() -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)
    with gzip.open(DATA_FILE, mode="rt", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                letter, _, _, _, metrics = line.strip().split("\t")
                totals[letter] += sum(int(pair.split(":")[1]) for pair in metrics.split(","))
    return dict(sorted(totals.items()))
