from collections import defaultdict
import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


# Usa conjuntos por clave numerica para eliminar duplicados en O(1) antes de ordenar alfabeticamente.
def pregunta_08() -> list[tuple[int, list[str]]]:
    grouped: dict[int, set[str]] = defaultdict(set)
    with gzip.open(DATA_FILE, mode="rt", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                letter, raw_value, *_ = line.split("\t")
                grouped[int(raw_value)].add(letter)
    return [(value, sorted(letters)) for value, letters in sorted(grouped.items())]
