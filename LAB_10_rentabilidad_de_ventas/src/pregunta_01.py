from pathlib import Path

import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """

    base_dir = Path(__file__).resolve().parents[1]
    data_path = base_dir / "data" / "superstore_orders.csv.gz"
    submission_dir = base_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path, sep=";", decimal=",")

    lines_count = len(df)
    orders_count = df["Order ID"].nunique()
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    profit_margin = total_profit / total_sales
    loss_lines = (df["Profit"] < 0).sum()
    loss_line_rate = loss_lines / lines_count
    lost_profit = abs(df.loc[df["Profit"] < 0, "Profit"].sum())

    profitability_summary = pd.DataFrame(
        [
            {
                "lines": lines_count,
                "orders": orders_count,
                "sales": total_sales,
                "profit": total_profit,
                "profit_margin": profit_margin,
                "loss_lines": loss_lines,
                "loss_line_rate": loss_line_rate,
                "lost_profit": lost_profit,
            }
        ]
    )

    def get_discount_band(d):
        if d == 0:
            return "0%"
        elif d <= 0.05:
            return "1%-5%"
        elif d <= 0.10:
            return "6%-10%"
        return "más de 10%"

    df["discount_band"] = df["Discount"].apply(get_discount_band)

    bands = ["0%", "1%-5%", "6%-10%", "más de 10%"]
    disc_rows = []
    for band in bands:
        sub = df[df["discount_band"] == band]
        sub_sales = sub["Sales"].sum()
        sub_profit = sub["Profit"].sum()
        sub_lost = abs(sub.loc[sub["Profit"] < 0, "Profit"].sum())
        disc_rows.append(
            {
                "discount_band": band,
                "lines": len(sub),
                "sales": sub_sales,
                "profit": sub_profit,
                "profit_margin": sub_profit / sub_sales if sub_sales != 0 else 0.0,
                "loss_line_rate": (sub["Profit"] < 0).mean() if len(sub) > 0 else 0.0,
                "lost_profit": sub_lost,
            }
        )
    discount_summary = pd.DataFrame(disc_rows)

    seg_rows = []
    for (seg, cat), sub in df.groupby(["Customer Segment", "Product Category"]):
        if len(sub) >= 100:
            sub_sales = sub["Sales"].sum()
            sub_profit = sub["Profit"].sum()
            sub_lost = abs(sub.loc[sub["Profit"] < 0, "Profit"].sum())
            seg_rows.append(
                {
                    "Customer Segment": seg,
                    "Product Category": cat,
                    "lines": len(sub),
                    "sales": sub_sales,
                    "profit": sub_profit,
                    "profit_margin": sub_profit / sub_sales if sub_sales != 0 else 0.0,
                    "lost_profit": sub_lost,
                }
            )

    priority_segments = (
        pd.DataFrame(seg_rows)
        .sort_values("lost_profit", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )

    profitability_summary.to_csv(submission_dir / "profitability_summary.csv", index=False)
    discount_summary.to_csv(submission_dir / "discount_summary.csv", index=False)
    priority_segments.to_csv(submission_dir / "priority_segments.csv", index=False)

    return profitability_summary, discount_summary, priority_segments
