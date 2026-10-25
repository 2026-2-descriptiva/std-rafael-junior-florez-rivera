from collections import defaultdict
import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


# Agrupa letras en listas con defaultdict(list) para preservar repetidos y el orden de aparicion.
def pregunta_07() -> list[tuple[int, list[str]]]:
    grouped: dict[int, list[str]] = defaultdict(list)
    with gzip.open(DATA_FILE, mode="rt", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                letter, raw_value, *_ = line.split("\t")
                grouped[int(raw_value)].append(letter)
    return sorted(grouped.items())
