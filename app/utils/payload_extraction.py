import json
import os
import re
from typing import Any

import pandas as pd


def get_final_response(output_steps: list[dict[str, Any]]) -> str | None:
    """
    Extracts the final assistant message from the Databricks execution steps.
    """
    for step in reversed(output_steps):
        if step.get("type") == "message" and step.get("role") == "assistant":
            content = step.get("content", [])
            if content and content[0].get("type") == "output_text":
                return content[0].get("text")


def extract_charts_from_payload(
    output_steps: list[dict[str, Any]],
) -> list[tuple[pd.DataFrame, str]]:
    """
    Parses function call outputs to find chart data and converts them into DataFrames.
    """
    charts = []
    CHART_DATA_JSON_FUNCTION = os.getenv("CHART_DATA_JSON_FUNCTION")

    if not CHART_DATA_JSON_FUNCTION:
        raise ValueError("Missing environment variable: CHART_DATA_JSON_FUNCTION")

    # Processes steps in logical order to maintain sequence
    for step in reversed(output_steps):
        if step.get(
            "type"
        ) == "function_call_output" and CHART_DATA_JSON_FUNCTION in step.get("name"):
            try:
                raw_output = step.get("output", "{}")
                db_json = json.loads(raw_output)

                inner_json_string = db_json.get("rows", [["{}"]])[0][0]
                chart_data = json.loads(inner_json_string)

                tipo_grafico = chart_data.get("tipo_grafico", "coluna")
                eixos = chart_data.get("eixos", [])

                if len(eixos) == 2:
                    eixo_x = next((e for e in eixos if e.get("eixo") == "x"), eixos[0])
                    eixo_y = next((e for e in eixos if e.get("eixo") == "y"), eixos[1])

                    col_x = eixo_x["coluna_origem"]
                    val_x = eixo_x["valores"]

                    col_y = eixo_y["coluna_origem"]
                    val_y = eixo_y["valores"]

                    df = pd.DataFrame({col_x: val_x, col_y: val_y})
                    df[col_x] = df[col_x].astype(str)

                    charts.append((df, tipo_grafico))
            except Exception as e:
                print(f"Error parsing chart JSON: {e}")

    return charts


def split_text_for_table(output: str) -> list[str]:
    """
    Splits the LLM response to isolate markdown tables using regex.
    """
    table_pattern = r"((?:^[^\n\r]*\|[^\n\r]*(?:\r?\n|$)){2,})"
    parts = re.split(table_pattern, output, flags=re.MULTILINE)
    return parts


def convert_markdown_table(markdown_table: str) -> pd.DataFrame | None:
    """
    Parses a raw markdown table string into a structured Pandas DataFrame.
    """
    items = [item.strip().replace("*", "") for item in markdown_table.split("|")]
    valid_items = [item for item in items if item != ""]

    if not valid_items:
        return pd.DataFrame()

    # Identify column quantity by finding the separator line (|---|)
    col_qty = 0
    for i, item in enumerate(valid_items):
        if re.match(r"^:?-+:?$", item):
            col_qty = i
            break

    if col_qty == 0:
        raise ValueError("Could not identify markdown table format.")

    # Slice header and raw data rows
    cols = valid_items[:col_qty]
    raw_data = valid_items[col_qty * 2 :]

    # Reshape flat list into matrix rows
    grouped_data = [raw_data[i : i + col_qty] for i in range(0, len(raw_data), col_qty)]

    return pd.DataFrame(grouped_data, columns=cols)
