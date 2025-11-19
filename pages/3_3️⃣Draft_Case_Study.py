import streamlit as st
from core.auth import require_password
from core.rag import query
from core.llm import chat
from core.nav import next_page

st.set_page_config(page_title="Draft Case Study", page_icon="📄", layout="wide")
require_password()

st.title("📄 Step 3 — Draft Case Study (RAG)")

answers = st.session_state.get("answers", {})
if not answers:
    st.warning("Please complete **Step 2 — Fill Missing Info** first.")
    st.stop()

topic_hint = st.text_input(
    "Optional: topic hint for better grounding",
    value="finance transformation, case study",
)

st.markdown(
    "When you click **Draft Now**, the app will:\n"
    "- 🔍 Use **RAG** to fetch relevant snippets from your uploaded materials\n"
    "- 🧠 Combine them with your answers to draft the case study"
)

if st.button("Draft Now"):
    answers_text = "\n".join([f"{k}: {v}" for k, v in answers.items() if v.strip()])
    retrieval_query = (answers_text + "\n\n" + topic_hint).strip()

    ctx_docs = query(retrieval_query, k=10)
    context_text = "\n\n".join([d.get("text", "") for d in ctx_docs]) or "(no retrieved context)"

    prompt = f"""You are a professional case study writer for public-sector finance.

Use BOTH:
1) CONTEXT: excerpts from source materials
2) USER ANSWERS: structured information from a form

to draft a polished, visually engaging case study with the following sections:

1) Captivating Title
2) Executive Summary (3–5 sentences)
3) Problem / Need for the project
4) Implementation Approach (timeline, roles, tools, governance)
5) Benefits & Impact (quantify where possible)
6) Key Learning Points (bulleted)
7) Point of Contact (POC: name, role, email — use placeholders if missing)
8) Suggested Visuals/Diagrams (list 2–3 ideas)

Make sure the narrative aligns closely with the CONTEXT, and only fill gaps using reasonable inference.

CONTEXT (retrieved via RAG):
-----------------------------
{context_text}

USER ANSWERS:
-------------
{answers_text}

Return **Markdown only**.
"""
    draft = chat([{"role": "user", "content": prompt}])
    st.session_state["case_markdown"] = draft
    st.success("✅ Draft ready. See below and proceed to **4️⃣ Generate Visuals**.")
    st.markdown(draft)

st.divider()
if st.session_state.get("case_markdown"):
    if st.button("Next → Generate Visuals"):
        next_page("pages/4_Generate_Visuals.py")
