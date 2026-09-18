import csv
import json
from pathlib import Path

from nicegui import ui


def convert_csv_2_json(input_file):
    project_root = Path(__file__).resolve().parents[2]
    candidates = []

    if input_file is None:
        raise FileNotFoundError("No file name was provided.")

    input_path = Path(input_file)
    if input_path.is_absolute():
        candidates.append(input_path)
    else:
        candidates.extend(
            [
                Path.cwd() / input_file,
                project_root / input_file,
                project_root / "PRE_03_csv2json" / input_file,
                project_root / "PRE_03_csv2json" / "data" / input_file,
            ]
        )

    resolved_input = next((path for path in candidates if path.exists()), None)
    if resolved_input is None:
        raise FileNotFoundError(f"No se encontró el archivo: {input_file}")

    output_file = project_root / "PRE_03_csv2json" / "temp" / f"{resolved_input.stem}.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    data = []
    with open(resolved_input, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    ui.notify("The file was transformed successfully!")


def app():
    """Main function to run the app"""

    ui.label("CSV to JSON Converter").classes("text-4xl font-bold")
    ui.label("")

    filename = ui.input(
        label="CSV file to convert:",
        placeholder="filename",
    )

    ui.label("")

    ui.label("")
    ui.button("Convert", on_click=lambda: convert_csv_2_json(filename.value))
    ui.run(port=8081)


if __name__ in {"__main__", "__mp_main__"}:
    app()


