import random
import time
from typing import Any

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from .payload_extraction import convert_markdown_table
from .plot_chart import plot_chart


def get_custom_css() -> str:
    """
    Custom CSS to inject into the Streamlit application for better
    aesthetics and branding.
    """
    return """
        <style>
            [data-testid="stHeader"] {
                background-color: #FFFFFF !important;
            }

            /* Hide default deploy button */
            .stAppDeployButton {
                display: none;
            }

            h1 {
                padding-top: 0px !important;
            }

            .st-key-header-container {
                position: fixed;
                top: 0px;
                left: 0px;
                right: 0px;
                z-index: 9999;
                padding: 3rem 5rem 1rem 5rem;
                background-color: #FFFFFF;
                border-bottom: 1px solid #e6e6e6;
            }

            .block-container {
                padding-top: 200px;
                padding-bottom: 0rm;
                padding-left: 5rem;
                padding-right: 5rem;
            }

            /* Sidebar history button styles */
            button[data-testid="stBaseButton-tertiary"],
            button[data-testid="stBaseButton-secondary"] {
                text-align: left !important;
                justify-content: flex-start !important;
                border-radius: 4px !important;
                padding: 6px 12px !important;
                margin-bottom: 2px !important;
                font-size: 14px !important;
                font-weight: 400 !important;
                transition: background-color 0.2s ease !important;
                border: none !important;
                height: auto !important;
                background-color: transparent !important;
            }

            /* Unselected Chat Style */
            button[data-testid="stBaseButton-tertiary"] {
                color: #555 !important;
                background-color: #f8f9fb !important;
                border: 1px solid #f0f2f6 !important;
            }

            button[data-testid="stBaseButton-tertiary"]:hover {
                background-color: #f0f2f6 !important;
                color: #1b5162 !important;
                border: 1px solid #e0e0e0 !important;
            }

            /* Selected Chat Style - Subtle and Discrete */
            button[data-testid="stBaseButton-secondary"] {
                background-color: #f0f7f9 !important;
                color: #1b5162 !important;
                font-weight: 600 !important;
                border-left: 3px solid #1b5162 !important;
                border-radius: 0 4px 4px 0 !important;
            }

            button[data-testid="stBaseButton-secondary"]:hover {
                background-color: #e6f1f5 !important;
            }

            .reportview-container {
                margin-top: -2em;
            }

            #MainMenu {
                visibility: hidden;
            }

            .stDeployButton {
                display:none;
            }

            footer {
                visibility: hidden;
            }

            #stDecoration {
                display:none;
            }
        </style>
        """


def get_mangueiras_questions() -> list[str]:
    """
    Returns a curated list of sample questions for the chat placeholder.
    """
    return [
        "Qual o top 5 faturamento de mangueiras?",
        "Quais são as 5 mangueiras que mais faturam?",
        "Me mostre o top 5 de mangueiras por faturamento.",
        "Quais as 5 mangueiras com a maior receita?",
        "Liste as 5 mangueiras que geram mais dinheiro na empresa.",
        "Qual é o ranking top 5 de receita no segmento de mangueiras?",
        "Me dê as 5 mangueiras mais vendidas em valor monetário.",
        "Quais mangueiras ocupam as 5 primeiras posições em faturamento?",
        "Pode listar as 5 mangueiras com maior volume de vendas em R$?",
        "Exiba o top 5 de faturamento da categoria de mangueiras.",
        "Quais são os cinco tipos de mangueira que mais dão retorno financeiro?",
        "Mostre-me as 5 mangueiras mais rentáveis no momento.",
        "Qual o top 5 de vendas brutas para os produtos tipo mangueira?",
        "Quais as top 5 mangueiras em termos de receita total?",
        "Quais são os 5 principais itens de mangueiras considerando o faturamento?",
    ]


def get_random_placeholder() -> str:
    return f"Ex: {random.choice(get_mangueiras_questions())}"


def scroll_to_bottom() -> None:
    """
    JavaScript injection to force the window to scroll to the latest message.
    """
    uid = time.time()

    js = f"""
    <script>
        // Execução: {uid}
        var main = window.parent.document.querySelector('.stMain');
        var app = window.parent.document.querySelector('.stApp');
        var body = main || app;
        if (body) {{
            body.scrollTo({{top: body.scrollHeight, behavior: 'smooth'}});
        }} else {{
            window.parent.scrollTo(0, window.parent.document.body.scrollHeight);
        }}
    </script>
    """
    components.html(js, height=0)


def render_complex_response(
    text_list: list[str],
    charts_data: list[tuple[pd.DataFrame, str]] | None = None,
    msg_index: int | str = "new",
) -> tuple[list[pd.DataFrame], list[Any]]:
    """
    Iterates through text parts to render tables and Plotly charts
    within the dashboard.
    """
    saved_dfs: list[pd.DataFrame] = []
    saved_figs: list[Any] = []

    # Render text and markdown tables
    for i, part in enumerate(text_list):
        if i % 2 == 0:
            if part.strip():
                st.markdown(part.replace("$", "&#36;"))
        else:
            try:
                df_md = convert_markdown_table(part)
                if df_md is not None and not df_md.empty:
                    st.dataframe(df_md)
                    saved_dfs.append(df_md)
                else:
                    st.markdown(part.replace("$", "&#36;"))
            except Exception:
                st.markdown(part.replace("$", "&#36;"))

    # Render charts if provided
    if charts_data:
        for idx, (chart_df, tipo_grafico) in enumerate(charts_data):
            if chart_df is not None and not chart_df.empty:
                try:
                    fig = plot_chart(chart_df, chart_type=tipo_grafico)
                    st.plotly_chart(
                        fig,
                        key=f"dynamic_chart_{msg_index}_{idx}",
                    )
                    saved_figs.append(fig)
                except Exception as e:
                    msg_err = f"Erro ao plotar gráfico {idx+1}: {e}"
                    st.error(msg_err)

    return saved_dfs, saved_figs
