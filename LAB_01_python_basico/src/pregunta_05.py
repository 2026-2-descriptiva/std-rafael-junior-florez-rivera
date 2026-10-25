import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


# Mantiene solo los extremos (maximo, minimo) por letra en una pasada sin almacenar listas completas.
def pregunta_05() -> list[tuple[str, int, int]]:
    bounds: dict[str, tuple[int, int]] = {}
    with gzip.open(DATA_FILE, mode="rt", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                letter, raw_value, *_ = line.split("\t")
                value = int(raw_value)
                if letter in bounds:
                    high, low = bounds[letter]
                    bounds[letter] = (max(high, value), min(low, value))
                else:
                    bounds[letter] = (value, value)
    return [(letter, high, low) for letter, (high, low) in sorted(bounds.items())]
