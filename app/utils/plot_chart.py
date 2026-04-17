from typing import Any

import pandas as pd
import plotly.express as px


def plot_chart(
    df: pd.DataFrame,
    chart_type: str = "coluna",
    x_col: str | None = None,
    y_col: str | None = None,
    title: str | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
    color_scale: str = "Blues",
) -> Any:
    """
    Generates a Plotly figure based on the provided DataFrame and requested chart type.
    """
    # Default to first two columns if names are not provided
    x_col = x_col if x_col else df.columns[0]
    y_col = y_col if y_col else df.columns[1]

    x_label = x_label if x_label else str(x_col).title()
    y_label = y_label if y_label else str(y_col).title()

    title = title if title else f"{y_label.capitalize()} por {x_label}"
    chart_type = str(chart_type).strip().lower()

    if chart_type == "linha":
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            title=title,
            labels={x_col: x_label, y_col: y_label},
            markers=True,
        )
        fig.update_traces(line_color="#1b5162", line_width=3, marker_size=8)

    elif chart_type == "pizza":
        fig = px.pie(
            df,
            names=x_col,
            values=y_col,
            title=title,
            labels={x_col: x_label, y_col: y_label},
            color_discrete_sequence=px.colors.sequential.Blues_r,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")

    elif chart_type == "barra":
        df[y_col] = df[y_col].astype(str)

        # Horizontal layout for labels readability
        fig = px.bar(
            df,
            x=y_col,
            y=x_col,
            orientation="h",
            title=title,
            labels={y_col: y_label, x_col: x_label},
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        fig.update_yaxes(type="category")

    else:
        # Default vertical bar chart
        df[x_col] = df[x_col].astype(str)

        fig = px.bar(
            df, x=x_col, y=y_col, title=title, labels={x_col: x_label, y_col: y_label}
        )
        # Ensure categorical axis to prevent numerical gaps
        fig.update_xaxes(type="category")

    return fig
