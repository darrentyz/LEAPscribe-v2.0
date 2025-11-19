import os
import streamlit as st
from graphviz import Digraph

st.set_page_config(page_title="About Us", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About Us")

# 👉 Update these paths if your images are elsewhere
PROCESS_FLOW_IMG = "/mnt/data/f8ad487b-6b1f-4432-a8ed-ad52e516c92a.png"
ARCHITECTURE_IMG = "data/architecture.png"

# ---- Helpers to render diagrams when images aren't available ----
def render_process_flow():
    g = Digraph("process", format="png")
    g.attr(rankdir="LR", splines="ortho", nodesep="0.5", ranksep="0.6")
    g.attr("node", shape="rounded", style="filled", fillcolor="#f6f8fa")

    g.node("U1", "1) Upload & Analyze")
    g.node("U2", "2) Fill Missing Info")
    g.node("U3", "3) Draft Case Study (RAG)")
    g.node("U4", "4) Generate Visuals")
    g.node("U5", "5) Map Capabilities")
    g.node("U6", "6) Summary & Download")
    g.node("U7", "7) Chat with Materials")

    g.edges([("U1","U2"), ("U2","U3"), ("U3","U4"), ("U4","U5"), ("U5","U6")])
    g.edge("U6","U7", label="(optional)")

    return g

def render_architecture():
    g = Digraph("arch", format="png")
    g.attr(rankdir="LR", splines="ortho", nodesep="0.5", ranksep="0.6")
    g.attr("node", shape="box", style="filled", fillcolor="#eef4ff")

    g.node("ST", "Streamlit App\n(pages 1–7)")
    g.node("LC", "LangChain\n(RAG)")
    g.node("VS", "FAISS Index\n(data/faiss_langchain)")
    g.node("EMB", "OpenAI Embeddings\n(text-embedding-3-small)")
    g.node("LLM", "OpenAI Chat\n(gpt-4o-mini)")
    g.node("IMG", "OpenAI Images\n(gpt-image-1)")
    g.node("DOCX", "DOCX Export\n(python-docx)")

    g.edge("ST", "LC", label="queries")
    g.edge("LC", "VS", label="similarity search")
    g.edge("LC", "EMB", label="embed")
    g.edge("ST", "LLM", label="draft, Q&A")
    g.edge("ST", "IMG", label="generate visuals")
    g.edge("ST", "DOCX", label="build & download")

    return g

# ---- Images or diagrams ----
st.subheader("📈 Process Flow")
if os.path.exists(PROCESS_FLOW_IMG):
    st.image(PROCESS_FLOW_IMG, caption="LEAPscribe Process Flow", use_column_width=True)
else:
    st.graphviz_chart(render_process_flow())

st.subheader("🏗️ Architecture Overview")
if os.path.exists(ARCHITECTURE_IMG):
    st.image(ARCHITECTURE_IMG, caption="LEAPscribe Architecture", use_column_width=True)
else:
    st.graphviz_chart(render_architecture())

st.markdown(
"""
### Problem Statement

Agencies across the WOG Finance community are often reluctant to share their success
stories on the Learn & LEAP Portal. Common reasons include:
- Limited time to write  
- Lack of confidence in crafting compelling narratives  
- Uncertainty about what details to include  

This results in valuable lessons remaining siloed within individual agencies.

### Our Solution — LEAPscribe

LEAPscribe is an AI-assisted case study wizard that:
- Ingests raw artefacts (slides, reports, emails)  
- Identifies missing information and prompts users with targeted questions  
- Drafts a polished, visually engaging case study  
- Generates visuals/diagrams to bring the story to life  
- Maps the case study to finance capabilities and best practice statements

### Outcomes

- **Lower barrier to sharing** — Agencies produce case studies with far less effort.  
- **Richer knowledge base** — More consistent, high-quality case studies on Learn & LEAP.  
- **Stronger institutional memory** — Stories are tagged to capabilities for reuse and replication across WOG Finance.
"""
)
