from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SUBMISSION_DIR = BASE_DIR / "submission"


# Recorre categorias y archivos en orden lexicografico determinista para consolidar frases limpias por particion.
def _load_split(split_dir: Path) -> pd.DataFrame:
    rows = [
        {"phrase": txt_file.read_text(encoding="utf-8").strip(), "target": category_dir.name}
        for category_dir in sorted(p for p in split_dir.iterdir() if p.is_dir())
        for txt_file in sorted(category_dir.glob("*.txt"))
    ]
    return pd.DataFrame(rows, columns=["phrase", "target"])


# Exporta los conjuntos train y test sin indice para cumplir el contrato de evaluacion en submission/.
def pregunta_01() -> None:
    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    for split in ("train", "test"):
        df = _load_split(DATA_DIR / split)
        df.to_csv(SUBMISSION_DIR / f"{split}_dataset.csv", index=False, encoding="utf-8")
