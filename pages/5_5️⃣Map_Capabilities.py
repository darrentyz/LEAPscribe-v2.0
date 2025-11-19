import streamlit as st
from core.auth import require_password
from core.llm import chat
from core.utils import get_all_best_practices, parse_bp_ids
from core.nav import next_page

st.set_page_config(page_title="Map Capabilities", page_icon="🧩", layout="wide")
require_password()

st.title("🧩 Step 5 — Map Capabilities & Best Practice Statements")

case_md = st.session_state.get("case_markdown")
if not case_md:
    st.warning("Please complete **Step 3 – Draft Case Study** first.")
    st.stop()

bps = get_all_best_practices()
bp_by_id = {bp["metric_id"]: bp for bp in bps}

st.markdown(
    "The AI will suggest which **capabilities and best practice statements** best match "
    "this case study. You can then refine the selection."
)

with st.expander("View case study draft"):
    st.markdown(case_md)

if st.button("🤖 Suggest Best Practice Statements"):
    bp_list_str = "\n".join(
        f"{bp['metric_id']}: {bp['capability']} – {bp['statement']}"
        for bp in bps
    )
    prompt = f"""You are mapping a finance transformation case study to a capability framework.

You are given:
1) The CASE STUDY text.
2) A list of CAPABILITY BEST PRACTICE STATEMENTS, each with a metric ID.

Task:
- Select ALL best practice statements that clearly apply to this case.
- Return only their metric IDs as a bullet list (e.g. "- 1.1.1").

CASE STUDY:
----------------
{case_md[:6000]}

CAPABILITY BEST PRACTICE STATEMENTS:
----------------
{bp_list_str}
"""
    out = chat([{"role": "user", "content": prompt}])
    st.session_state["bp_suggestion_raw"] = out
    suggested_ids = parse_bp_ids(out)
    st.session_state["bp_suggested_ids"] = suggested_ids

    st.success("✅ Suggested best practice statements identified.")
    with st.expander("See raw AI suggestion"):
        st.markdown(out)

suggested_ids = st.session_state.get("bp_suggested_ids", [])
all_ids = [bp["metric_id"] for bp in bps]

st.subheader("Select best practice statements that apply")

default_ids = suggested_ids if suggested_ids else []
selected_ids = st.multiselect(
    "Select all that best represent this case study:",
    options=all_ids,
    default=default_ids,
    format_func=lambda mid: f"{mid} – {bp_by_id[mid]['statement']}",
)

if st.button("💾 Save Selection"):
    selected_bps = [bp_by_id[mid] for mid in selected_ids]
    st.session_state["selected_best_practices"] = selected_bps
    st.success(f"Saved {len(selected_bps)} best practice statements.")

if st.session_state.get("selected_best_practices"):
    st.markdown("### Currently Saved Selection")
    for bp in st.session_state["selected_best_practices"]:
        st.markdown(
            f"- **{bp['cap_id']} {bp['capability']}** – `{bp['metric_id']}`: {bp['statement']}"
        )

st.divider()
if st.session_state.get("selected_best_practices"):
    if st.button("Next → Summary & Download"):
        next_page("pages/6_6️⃣Summary_&_Download.py")
