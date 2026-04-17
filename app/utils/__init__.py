from .handle_request import handle_request
from .payload_extraction import (
    extract_charts_from_payload,
    get_final_response,
    split_text_for_table
)
from .ui_utils import (
    get_custom_css,
    get_mangueiras_questions,
    get_random_placeholder,
    scroll_to_bottom,
    render_complex_response
)
from .db_utils import (
    save_or_update_chat,
    get_chat_messages,
    get_user_chats
)
