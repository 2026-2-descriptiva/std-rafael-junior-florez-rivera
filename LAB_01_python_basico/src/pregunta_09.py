from collections import Counter
import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


# Cuenta claves de metricas con Counter y reconstruye el diccionario ordenado alfabeticamente.
def pregunta_09() -> dict[str, int]:
    counts: Counter[str] = Counter()
    with gzip.open(DATA_FILE, mode="rt", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                metrics = line.strip().split("\t")[4]
                counts.update(pair.split(":")[0] for pair in metrics.split(","))
    return dict(sorted(counts.items()))
