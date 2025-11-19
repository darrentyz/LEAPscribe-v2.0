import streamlit as st
from core.auth import require_password
from core.rag import extract_text, upsert_documents, clear_index
from core.llm import chat
from core.utils import parse_questions_list
from core.nav import next_page

st.set_page_config(page_title="Upload & Analyze", page_icon="📤", layout="wide")
require_password()

st.title("📤 Step 1 — Upload & Analyze")

with st.expander("Admin actions"):
    if st.button("🧹 Reset Knowledge Base (clear vector index)"):
        clear_index()
        st.session_state.pop("missing_questions", None)
        st.session_state.pop("missing_questions_text", None)
        st.success("Knowledge base cleared.")

uploads = st.file_uploader(
    "Upload files (PDF/DOCX/TXT)",
    type=["pdf", "docx", "txt", "md"],
    accept_multiple_files=True,
)

if st.button("Ingest & Analyze") and uploads:
    texts = []
    docs_for_index = []

    for f in uploads:
        raw = f.read()
        t = extract_text(raw, f.name)
        texts.append(t)
        docs_for_index.append(
            {
                "text": t,
                "meta": {"filename": f.name, "source": "user_upload"},
            }
        )

    upsert_documents(docs_for_index)
    st.success("✅ Ingested & indexed documents into the knowledge base.")

    corpus_sample = "\n\n".join([t[:1500] for t in texts])[:4000]
    prompt = f"""You are assisting to prepare a public-sector finance CASE STUDY.

Based on the following uploaded content (may be partial), list the
MISSING INFORMATION we must ask the user as bullet questions.

Cover:
- title direction
- executive summary angle
- problem clarity
- implementation specifics (timeline, roles, tools)
- benefits with metrics
- key learning points
- POC contact details

Content sample:
---
{corpus_sample}
---

Return only bullet questions (can be 0, max 3).
"""
    qs = chat([{"role": "user", "content": prompt}])

    st.session_state["missing_questions_text"] = qs
    st.session_state["missing_questions"] = parse_questions_list(qs)

    st.success("🔎 Analysis complete. Proceed to **2️⃣ Fill Missing Info**.")
    with st.expander("See suggested questions"):
        st.markdown(qs)

st.divider()
if st.session_state.get("missing_questions"):
    if st.button("Next → Fill Missing Info"):
        next_page("pages/2_Fill_Missing_Info.py")
