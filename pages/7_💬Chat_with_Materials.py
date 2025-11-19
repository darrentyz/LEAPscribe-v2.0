import streamlit as st
from core.auth import require_password
from core.rag import query
from core.llm import chat

st.set_page_config(page_title="Chat with Materials", page_icon="💬", layout="wide")
require_password()

st.title("💬 Final Step — Chat with Your Case Study & Materials")

st.markdown(
"""
Ask questions about your **uploaded artefacts** or the **generated case study**.

- **RAG mode**: searches the LangChain FAISS index of uploaded materials.  
- **Case study mode**: answers based only on the final case study text.
"""
)

case_md = st.session_state.get("case_markdown")

mode = st.radio(
    "Choose what to chat with:",
    ["Uploaded materials (RAG)", "Final case study only"],
)

if mode == "Final case study only" and not case_md:
    st.warning("No case study draft found. Please complete the drafting step first.")
    st.stop()

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for role, content in st.session_state["chat_history"]:
    st.chat_message(role).markdown(content)

user_input = st.chat_input("Ask a question about your materials or case study...")
if not user_input:
    st.stop()

st.session_state["chat_history"].append(("user", user_input))
st.chat_message("user").markdown(user_input)

if mode == "Uploaded materials (RAG)":
    ctx_docs = query(user_input, k=8)
    if not ctx_docs:
        answer = (
            "I couldn't find any indexed content yet. "
            "Please go to **Step 1 – Upload & Analyze** to ingest documents first."
        )
        st.session_state["chat_history"].append(("assistant", answer))
        st.chat_message("assistant").markdown(answer)
        st.stop()

    context_text = "\n\n".join(d.get("text", "") for d in ctx_docs)
    sys_msg = (
        "You are answering questions about uploaded public-sector finance case materials. "
        "Use the provided CONTEXT to answer as accurately as possible. "
        "If something is not clearly supported by the context, say you are not certain."
    )
    prompt = f"""CONTEXT (retrieved from uploaded materials):
-------------------------------------------
{context_text}

QUESTION:
---------
{user_input}
"""
else:
    context_text = case_md or ""
    sys_msg = (
        "You are answering questions about the following case study. "
        "Base your answers strictly on the case study text."
    )
    prompt = f"""CASE STUDY:
-----------
{context_text}

QUESTION:
---------
{user_input}
"""

assistant_reply = chat(
    [
        {"role": "system", "content": sys_msg},
        {"role": "user", "content": prompt},
    ]
)

st.session_state["chat_history"].append(("assistant", assistant_reply))
st.chat_message("assistant").markdown(assistant_reply)

if mode == "Uploaded materials (RAG)":
    with st.expander("Show retrieved context (from uploaded materials)"):
        st.markdown(context_text)
