from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    base_dir = Path(__file__).resolve().parents[1]
    data_path = base_dir / "data" / "sales.csv.gz"
    submission_dir = base_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    df["order_period"] = df["OrderDate"].dt.to_period("M")

    cohorts = df.groupby("CustomerID")["order_period"].min().rename("cohort_period")
    df = df.merge(cohorts, on="CustomerID")

    df["period_index"] = (
        (df["order_period"].dt.year - df["cohort_period"].dt.year) * 12
        + (df["order_period"].dt.month - df["cohort_period"].dt.month)
    )
    df["cohort_month"] = df["cohort_period"].dt.strftime("%Y-%m")

    grouped = (
        df.groupby(["cohort_month", "period_index"])["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )
    cohort_sizes = (
        grouped[grouped["period_index"] == 0]
        .set_index("cohort_month")["active_customers"]
        .rename("cohort_size")
    )
    grouped = grouped.merge(cohort_sizes, on="cohort_month")
    grouped["retention_rate"] = (
        grouped["active_customers"] / grouped["cohort_size"]
    )
    grouped = grouped.sort_values(["cohort_month", "period_index"]).reset_index(
        drop=True
    )

    grouped.to_csv(submission_dir / "cohort_retention.csv", index=False)

    pivot = grouped.pivot(
        index="cohort_month", columns="period_index", values="retention_rate"
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    cax = ax.imshow(pivot.values, cmap="Blues", aspect="auto")
    fig.colorbar(cax)

    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)

    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.iloc[i, j]
            if pd.notna(val):
                ax.text(
                    j,
                    i,
                    f"{val:.1%}",
                    ha="center",
                    va="center",
                    color="white" if val > 0.5 else "black",
                )

    ax.set_title("Retention Rate by Cohort")
    ax.set_xlabel("Period Index")
    ax.set_ylabel("Cohort Month")
    fig.tight_layout()
    fig.savefig(submission_dir / "cohort_retention_heatmap.png")
    plt.close(fig)

    return grouped
