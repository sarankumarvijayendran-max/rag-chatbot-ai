import streamlit as st


# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------

def load_css():

    st.markdown("""
    <style>

    /* Main App */
    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a,
            #111827
        );
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Remove Streamlit Menu/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Header */
    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 700;
        color: white;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 18px;
        margin-bottom: 30px;
    }

    /* File uploader */
    section[data-testid="stFileUploader"] {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #334155;
    }

    /* Input */
    .stTextInput input {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 14px !important;
        border: 1px solid #334155 !important;
        padding: 14px !important;
    }

    /* Button */
    .stButton button {
        width: 100%;
        border-radius: 14px;
        height: 3.2em;
        background: linear-gradient(
            90deg,
            #7c3aed,
            #2563eb
        );
        color: white;
        font-size: 16px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }

    .stButton button:hover {
        transform: scale(1.02);
    }

    /* User Bubble */
    .user-msg {
        background: linear-gradient(
            135deg,
            #2563eb,
            #1d4ed8
        );

        padding: 16px;
        border-radius: 18px;
        margin-bottom: 12px;
        margin-left: auto;
        width: fit-content;
        max-width: 80%;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Bot Bubble */
    .bot-msg {
        background-color: #1e293b;
        padding: 16px;
        border-radius: 18px;
        margin-bottom: 20px;
        width: fit-content;
        max-width: 80%;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Chat Area */
    .chat-container {
        padding-top: 20px;
        padding-bottom: 20px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    </style>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

def render_header():

    st.markdown("""
    <div class="main-title">
        🤖 AI Document Assistant
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="subtitle">
        Upload PDF or Excel files and ask intelligent questions using RAG
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# CHAT UI
# --------------------------------------------------

def render_chat(chat_history):

    st.markdown(
        '<div class="chat-container">',
        unsafe_allow_html=True
    )

    for question, answer in chat_history[::-1]:

        # User Message
        st.markdown(
            f"""
            <div class="user-msg">
            🧑 <b>You</b><br><br>
            {question}
            </div>
            """,
            unsafe_allow_html=True
        )

        # AI Message
        st.markdown(
            f"""
            <div class="bot-msg">
            🤖 <b>AI Assistant</b><br><br>
            {answer}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )