from collections import defaultdict
import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


# Distribuye el valor entero del registro hacia cada codigo asociado y ordena las claves resultantes.
def pregunta_11() -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)
    with gzip.open(DATA_FILE, mode="rt", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                _, raw_value, _, codes, _ = line.strip().split("\t")
                value = int(raw_value)
                for code in codes.split(","):
                    totals[code] += value
    return dict(sorted(totals.items()))
