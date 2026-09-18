# clean.py

import os

import pandas as pd

INPUT_FILE = "PRE_04_limpieza/data/ventas.csv"
OUTPUT_FILE = "PRE_04_limpieza/submission/ventas.csv"



def main():

    df = pd.read_csv(INPUT_FILE)



    df.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()
