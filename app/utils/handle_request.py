import os
from typing import Any

import requests


def handle_request(payload: dict[str, Any]) -> requests.Response:
    databricks_vars = {
        "DATABRICKS_HOST": os.getenv("DATABRICKS_HOST"),
        "DATABRICKS_TOKEN": os.getenv("DATABRICKS_TOKEN"),
        "ENDPOINT_NAME": os.getenv("ENDPOINT_NAME"),
    }

    # Validate all required variables are set
    for var_name, var_value in databricks_vars.items():
        if not var_value:
            raise ValueError(f"Missing environment variable: {var_name}")

    DATABRICKS_HOST = databricks_vars["DATABRICKS_HOST"]
    DATABRICKS_TOKEN = databricks_vars["DATABRICKS_TOKEN"]
    ENDPOINT_NAME = databricks_vars["ENDPOINT_NAME"]

    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json",
    }

    return requests.post(
        f"{DATABRICKS_HOST}/serving-endpoints/{ENDPOINT_NAME}/invocations",
        headers=headers,
        json=payload,
        timeout=300,
    )
