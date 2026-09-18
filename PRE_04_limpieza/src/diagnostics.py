# diagnostics.py

import pandas as pd


OUTPUT_FILE = "PRE_04_limpieza/submission/ventas.csv"


def main():
    df = pd.read_csv(OUTPUT_FILE)
    series = df["supplier"]
    series = series.sort_values()
    print(df.head())


if __name__ == "__main__":
    main()
