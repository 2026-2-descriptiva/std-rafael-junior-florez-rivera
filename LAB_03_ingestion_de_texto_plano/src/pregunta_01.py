from pathlib import Path
import re
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "clusters_report.txt"
CLUSTER_HEADER = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$")


# Reconstruye registros multilinea mediante anclaje regex de inicio de cluster y normaliza espacios y puntuacion.
def pregunta_01() -> pd.DataFrame:
    records: list[dict[str, int | float | list[str]]] = []

    with open(DATA_FILE, mode="r", encoding="utf-8") as file:
        for line in list(file)[4:]:
            stripped = line.strip()
            if not stripped:
                continue
            if match := CLUSTER_HEADER.match(line):
                records.append(
                    {
                        "cluster": int(match.group(1)),
                        "cantidad_de_palabras_clave": int(match.group(2)),
                        "porcentaje_de_palabras_clave": float(match.group(3).replace(",", ".")),
                        "keywords": [match.group(4).strip()],
                    }
                )
            else:
                records[-1]["keywords"].append(stripped)

    rows = [
        {
            "cluster": item["cluster"],
            "cantidad_de_palabras_clave": item["cantidad_de_palabras_clave"],
            "porcentaje_de_palabras_clave": item["porcentaje_de_palabras_clave"],
            "principales_palabras_clave": ", ".join(
                " ".join(phrase.split())
                for phrase in " ".join(item["keywords"]).removesuffix(".").split(",")
            ),
        }
        for item in records
    ]
    return pd.DataFrame(rows)
