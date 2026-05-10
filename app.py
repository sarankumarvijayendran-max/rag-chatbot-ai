import os
import tempfile

import streamlit as st

from file_processor import (
    extract_text_from_pdf,
    extract_text_from_excel
)

from rag_engine import (
    build_vectorstore,
    generate_answer
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="NeuroDoc AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* --------------------------------------------------
MAIN APP
-------------------------------------------------- */

.stApp {
    background:
    radial-gradient(circle at top left,
    #1e293b 0%,
    #0f172a 45%,
    #020617 100%);

    color: white;
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* --------------------------------------------------
HEADER
-------------------------------------------------- */

.hero-title {

    font-size: 58px;
    font-weight: 800;

    text-align: center;

    background: linear-gradient(
        90deg,
        #38bdf8,
        #818cf8,
        #c084fc
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-top: 20px;
}

.hero-subtitle {

    text-align: center;

    color: #cbd5e1;

    font-size: 20px;

    margin-top: -10px;
    margin-bottom: 40px;
}

/* --------------------------------------------------
SIDEBAR
-------------------------------------------------- */

section[data-testid="stSidebar"] {

    background: rgba(15, 23, 42, 0.95);

    border-right: 1px solid rgba(
        255,
        255,
        255,
        0.08
    );

    backdrop-filter: blur(12px);
}

/* --------------------------------------------------
UPLOAD BOX
-------------------------------------------------- */

section[data-testid="stFileUploader"] {

    background: rgba(30, 41, 59, 0.8);

    border: 1px solid rgba(
        255,
        255,
        255,
        0.08
    );

    border-radius: 22px;

    padding: 22px;

    backdrop-filter: blur(10px);
}

/* --------------------------------------------------
TEXT INPUT
-------------------------------------------------- */

.stTextInput input {

    background: rgba(30, 41, 59, 0.85) !important;

    color: white !important;

    border-radius: 18px !important;

    border: 1px solid rgba(
        255,
        255,
        255,
        0.08
    ) !important;

    padding: 16px !important;

    font-size: 16px !important;
}

/* --------------------------------------------------
BUTTON
-------------------------------------------------- */

.stButton button {

    width: 100%;
    height: 3.4em;

    border-radius: 18px;

    border: none;

    font-size: 17px;
    font-weight: 700;

    color: white;

    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6,
        #ec4899
    );

    transition: all 0.3s ease;

    box-shadow: 0 8px 20px rgba(
        99,
        102,
        241,
        0.35
    );
}

.stButton button:hover {

    transform: translateY(-2px);

    box-shadow: 0 10px 25px rgba(
        139,
        92,
        246,
        0.5
    );
}

/* --------------------------------------------------
CHAT AREA
-------------------------------------------------- */

.chat-wrapper {

    margin-top: 25px;
}

/* USER MESSAGE */

.user-box {

    background: linear-gradient(
        135deg,
        #2563eb,
        #4f46e5
    );

    padding: 18px;

    border-radius: 22px;

    margin-bottom: 14px;

    margin-left: auto;

    width: fit-content;
    max-width: 78%;

    color: white;

    box-shadow: 0 8px 20px rgba(
        37,
        99,
        235,
        0.35
    );

    animation: fadeIn 0.3s ease;
}

/* AI MESSAGE */

.ai-box {

    background: rgba(30, 41, 59, 0.88);

    border: 1px solid rgba(
        255,
        255,
        255,
        0.06
    );

    padding: 18px;

    border-radius: 22px;

    margin-bottom: 24px;

    width: fit-content;
    max-width: 78%;

    color: #f8fafc;

    backdrop-filter: blur(12px);

    box-shadow: 0 8px 20px rgba(
        0,
        0,
        0,
        0.25
    );

    animation: fadeIn 0.3s ease;
}

/* --------------------------------------------------
ANIMATION
-------------------------------------------------- */

@keyframes fadeIn {

    from {
        opacity: 0;
        transform: translateY(8px);
    }

    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

/* --------------------------------------------------
FEATURE CARD
-------------------------------------------------- */

.feature-card {

    background: rgba(30, 41, 59, 0.7);

    border: 1px solid rgba(
        255,
        255,
        255,
        0.08
    );

    padding: 18px;

    border-radius: 20px;

    margin-bottom: 20px;

    backdrop-filter: blur(10px);

    color: white;
}

/* --------------------------------------------------
STATUS BOX
-------------------------------------------------- */

.status-box {

    background: rgba(15, 23, 42, 0.8);

    border: 1px solid rgba(
        255,
        255,
        255,
        0.06
    );

    padding: 14px;

    border-radius: 18px;

    text-align: center;

    margin-bottom: 15px;
}

/* --------------------------------------------------
SCROLLBAR
-------------------------------------------------- */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #475569;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown("""
<div class="hero-title">
NeuroDoc AI
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-subtitle">
AI-Powered PDF & Excel Intelligence Platform
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 📂 Upload Document")

    uploaded_file = st.file_uploader(
        "Upload PDF or Excel File",
        type=["pdf", "xlsx", "xls"]
    )

    st.markdown("---")

    st.markdown("""
    <div class="feature-card">

    <h4>⚡ AI Features</h4>

    ✅ Groq LLM <br>
    ✅ RAG Pipeline <br>
    ✅ FAISS Retrieval <br>
    ✅ Multi-sheet Excel <br>
    ✅ Semantic Search <br>
    ✅ Fast AI Responses

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="status-box">

    🚀 Powered by Llama 3.1

    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# FILE PROCESSING
# --------------------------------------------------

if uploaded_file:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(
            uploaded_file.name
        )[1]
    ) as tmp_file:

        tmp_file.write(
            uploaded_file.read()
        )

        tmp_path = tmp_file.name

    # PDF
    if uploaded_file.type == "application/pdf":

        text = extract_text_from_pdf(
            tmp_path
        )

    # Excel
    else:

        text = extract_text_from_excel(
            tmp_path
        )

    os.remove(tmp_path)

    with st.spinner(
        "🧠 Building AI Knowledge Base..."
    ):

        st.session_state.vectorstore = (
            build_vectorstore(text)
        )

    st.success(
        "✅ Document Indexed Successfully"
    )

# --------------------------------------------------
# CHAT SECTION
# --------------------------------------------------

st.markdown("## 💬 AI Chat")

st.markdown(
    '<div class="chat-wrapper">',
    unsafe_allow_html=True
)

for question, answer in st.session_state.chat_history[::-1]:

    # USER MESSAGE
    st.markdown(
        f"""
        <div class="user-box">

        🧑 <b>You</b><br><br>

        {question}

        </div>
        """,
        unsafe_allow_html=True
    )

    # AI MESSAGE
    st.markdown(
        f"""
        <div class="ai-box">

        🤖 <b>NeuroDoc AI</b><br><br>

        {answer}

        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    "</div>",
    unsafe_allow_html=True
)

# --------------------------------------------------
# QUESTION INPUT
# --------------------------------------------------

if st.session_state.vectorstore:

    user_question = st.text_input(
        "",
        placeholder="Ask anything from your document..."
    )

    ask_button = st.button(
        "🚀 Generate Intelligent Answer"
    )

    if ask_button and user_question:

        with st.spinner(
            "🤖 NeuroDoc AI is analyzing..."
        ):

            try:

                answer = generate_answer(
                    st.session_state.vectorstore,
                    user_question
                )

            except Exception as e:

                answer = f"Error: {str(e)}"

        st.session_state.chat_history.append(
            (
                user_question,
                answer
            )
        )

        st.rerun()

else:

    st.markdown("""
    <div class="feature-card"
    style="
        text-align:center;
        padding:40px;
        margin-top:30px;
    ">

    <h2>📂 Upload a Document</h2>

    <p style="color:#cbd5e1;font-size:18px;">

    Upload your PDF or Excel file and start
    chatting with your data using AI.

    </p>

    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Built with Streamlit • Groq • FAISS • LangChain"
)