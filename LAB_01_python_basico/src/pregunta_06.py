import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


# Desglosa cada par clave:valor actualizando (minimo, maximo) al vuelo para retornar el orden exigido.
def pregunta_06() -> list[tuple[str, int, int]]:
    bounds: dict[str, tuple[int, int]] = {}
    with gzip.open(DATA_FILE, mode="rt", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                metrics = line.strip().split("\t")[4]
                for pair in metrics.split(","):
                    key, raw_value = pair.split(":")
                    value = int(raw_value)
                    if key in bounds:
                        low, high = bounds[key]
                        bounds[key] = (min(low, value), max(high, value))
                    else:
                        bounds[key] = (value, value)
    return [(key, low, high) for key, (low, high) in sorted(bounds.items())]
