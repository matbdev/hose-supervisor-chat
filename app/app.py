import os

import streamlit as st
from utils import (
    extract_charts_from_payload,
    get_chat_messages,
    get_custom_css,
    get_final_response,
    get_random_placeholder,
    get_user_chats,
    handle_request,
    render_complex_response,
    save_or_update_chat,
    scroll_to_bottom,
    split_text_for_table,
)

# Page configuration
st.set_page_config(
    page_title="Chat - Mangueiras",
    page_icon=":speech_balloon:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Logo
logo_path = "app/assets/logo.png"
default_logo_path = "app/assets/matbdev-default-logo.png"

# Initialize session state for persistent variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "placeholder" not in st.session_state:
    st.session_state.placeholder = get_random_placeholder()

if "chat_thread_id" not in st.session_state:
    st.session_state.chat_thread_id = None

# Apply custom UI styling
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Header section with logo and title
with st.container(key="header-container"):
    _, col_logo, _ = st.columns([3, 1, 3], vertical_alignment="center")
    with col_logo:
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        else:
            st.image(default_logo_path, use_container_width=True)

    with st.container(horizontal_alignment="center", width="stretch"):
        st.title(
            "Consultor Especializado de Mangueiras",
            text_alignment="center",
            anchor=False,
        )

# Sidebar with conversation history
with st.sidebar:
    st.markdown("# Histórico")

    # Reset chat for a new session
    if st.button("Nova Conversa", width="stretch", type="primary"):
        st.session_state.messages = []
        st.session_state.chat_thread_id = None
        st.rerun()

    st.divider()

    # Fetch and display previous chats
    historico_chats = get_user_chats(user_id=1)

    if len(historico_chats) == 0:
        st.caption("Nenhuma conversa salva ainda.")
    else:
        for chat in historico_chats:
            tipo_botao = (
                "secondary"
                if st.session_state.chat_thread_id == chat["id"]
                else "tertiary"
            )

            if st.button(
                chat["title"],
                key=f"chat_{chat['id']}",
                width="stretch",
                type=tipo_botao,
            ):
                st.session_state.chat_thread_id = chat["id"]
                st.session_state.messages = get_chat_messages(chat["id"])
                st.rerun()

# Display current message history
for idx, msg in enumerate(st.session_state.messages):
    # Unique key
    thread_id = (
        st.session_state.chat_thread_id if st.session_state.chat_thread_id else "new"
    )
    unique_key = f"{thread_id}_{idx}"

    with st.chat_message(msg["role"]):
        if msg.get("is_error"):
            st.error(msg["content"])
        else:
            if msg["role"] == "assistant":
                st.markdown("**Resposta do Databricks**")

            # Extract and render charts/tables se vieram do Banco de Dados
            if (
                msg["role"] == "assistant"
                and "raw_data" in msg
                and "viz_list" not in msg
            ):
                output_steps = msg["raw_data"].get("output", [])
                charts = extract_charts_from_payload(output_steps)
                text_list = split_text_for_table(msg["content"])

                # Fixed key
                render_complex_response(
                    text_list, charts_data=charts, msg_index=unique_key
                )

            # Render if graphics are already processed in the current session
            elif msg["role"] == "assistant" and ("viz_list" in msg or "df_list" in msg):
                text_list = split_text_for_table(msg["content"])
                render_complex_response(text_list, msg_index=unique_key)

                if "viz_list" in msg:
                    for fig_idx, fig in enumerate(msg["viz_list"]):
                        st.plotly_chart(fig, key=f"dynamic_chart_{unique_key}_{fig_idx}")
            else:
                st.markdown(
                    msg["content"].replace("\n", "  \n")
                    if msg["role"] == "user"
                    else msg["content"]
                )

# Welcome screen shown only on empty sessions
welcome_placeholder = st.empty()
if len(st.session_state.messages) == 0:
    with welcome_placeholder.container(key="welcome_screen"):
        _, col_intro, _ = st.columns([1, 2, 1])
        with col_intro:
            for i in range(5):
                st.write("")

            st.info("""
            👋 **Bem-vindo ao Consultor Especializado de Mangueiras!**

            Estou integrado ao Databricks para ajudar com análises,
            especificações técnicas e geração de gráficos.
            Para começar, digite sua dúvida na barra abaixo.
            """)

            st.markdown("💡 **Exemplos do que você pode me perguntar:**")
            st.markdown("- *Mostre especificações técnicas de modelos específicos.*")
            st.markdown("- *Gere gráficos com dados de vendas do último trimestre.*")
            st.markdown("- *Compare os produtos mais vendidos do mês passado.*")

# Handle user input and API communication
if prompt := st.chat_input(st.session_state.placeholder, key="chat_input"):
    st.session_state.placeholder = get_random_placeholder()
    scroll_to_bottom()
    welcome_placeholder.empty()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt.replace("\n", "  \n"))

    scroll_to_bottom()

    # Prepare simplified message list for API consumption
    api_messages = []
    for m in st.session_state.messages:
        if not m.get("is_error"):
            api_messages.append({"role": m["role"], "content": m["content"]})

    payload = {"input": api_messages}

    with st.chat_message("assistant"):
        with st.spinner("O especialista está analisando sua pergunta..."):
            scroll_to_bottom()
            response = handle_request(payload)

        if response.status_code == 200:
            raw_data = response.json()
            output_steps = raw_data.get("output", [])

            final_text = get_final_response(output_steps)
            charts = extract_charts_from_payload(output_steps)
            text_list = split_text_for_table(final_text)

            st.markdown("**Resposta do Databricks**")

            # Unique key
            thread_id = (
                st.session_state.chat_thread_id
                if st.session_state.chat_thread_id
                else "new"
            )
            unique_key = f"{thread_id}_{len(st.session_state.messages)}"

            saved_dfs, saved_figs = render_complex_response(
                text_list,
                charts_data=charts,
                msg_index=unique_key,
            )

            saved_message = {
                "role": "assistant",
                "content": final_text,
                "raw_data": raw_data,
            }

            if saved_figs:
                saved_message["viz_list"] = saved_figs

            if saved_dfs:
                saved_message["df_list"] = saved_dfs

            st.session_state.messages.append(saved_message)

            # Sync conversation state with PostgreSQL
            db_messages = []
            for m in st.session_state.messages:
                if not m.get("is_error"):
                    msg_to_save = {"role": m["role"], "content": m["content"]}
                    if "raw_data" in m:
                        msg_to_save["raw_data"] = m["raw_data"]
                    db_messages.append(msg_to_save)

            new_id = save_or_update_chat(
                chat_id=st.session_state.chat_thread_id,
                messages=db_messages,
            )
            st.session_state.chat_thread_id = new_id

        else:
            status = response.status_code
            error_msg = f"Erro na comunicação com Databricks (Status {status})."
            st.error(error_msg)
            st.session_state.messages.append(
                {"role": "assistant", "content": error_msg, "is_error": True}
            )
