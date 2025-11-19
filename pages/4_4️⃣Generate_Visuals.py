import streamlit as st
from core.auth import require_password
from core.llm import chat, generate_image
from core.nav import next_page

st.set_page_config(page_title="Generate Visuals", page_icon="🖼️", layout="wide")
require_password()

st.title("🖼️ Step 4 — Generate Visuals")

draft = st.session_state.get("case_markdown")
if not draft:
    st.warning("Please complete **Step 3 — Draft Case Study** first.")
    st.stop()

st.subheader("Cover Illustration")
style = st.selectbox(
    "Style",
    ["flat illustration", "isometric", "line art", "minimal infographic"],
    index=0,
)
theme = st.text_input(
    "Theme keywords",
    value="public finance, collaboration, knowledge sharing, AI assistance, case studies",
)

if st.button("Generate Cover Image (1024x1024)"):
    prompt = (
        f"A {style} depicting {theme}. Clean, professional, government context, minimal color palette."
    )
    try:
        png_bytes = generate_image(prompt, size="1024x1024")
        st.image(png_bytes, caption="Cover Image", use_column_width=True)
        st.session_state["cover_image"] = png_bytes
        st.success("✅ Cover image generated.")
    except Exception as e:
        st.error(str(e))

st.divider()
st.subheader("Auto-create Simple Diagram Prompts")

if st.button("Suggest Diagram Prompts from Draft"):
    p = f"""From the following case study markdown, list three concise prompts for diagrams/flowcharts to visualise the process and impact.
Return bullet points only (max 3 prompts).
---
{draft[:5000]}
---"""
    out = chat([{"role": "user", "content": p}])
    st.session_state["diagram_prompts_raw"] = out
    prompts = [line.strip("-• ").strip() for line in out.splitlines() if line.strip()]
    st.session_state["diagram_prompts"] = prompts
    st.success("✅ Diagram prompts generated. Choose which to create below.")
    st.markdown(out)

prompts = st.session_state.get("diagram_prompts", [])
if prompts:
    st.subheader("Select diagrams to generate")
    selected = []
    for i, prompt in enumerate(prompts, start=1):
        if st.checkbox(f"{i}. {prompt}", key=f"diag_{i}"):
            selected.append(prompt)

    if selected and st.button("🎨 Generate Selected Diagrams"):
        generated_images = st.session_state.get("diagram_images", {})
        for p in selected:
            try:
                st.write(f"Generating: *{p}* ...")
                img_bytes = generate_image(
                    f"Professional flowchart or process diagram showing: {p}. Minimal style.",
                    size="1024x1024",
                )
                st.image(img_bytes, caption=p, use_column_width=True)
                generated_images[p] = img_bytes
            except Exception as e:
                st.error(f"Failed to generate diagram '{p}': {e}")
        st.session_state["diagram_images"] = generated_images
        st.success("✅ Selected diagrams generated.")

if st.session_state.get("cover_image") or st.session_state.get("diagram_images"):
    st.info("You can now proceed to **5️⃣ Map Capabilities**.")

st.divider()
if st.button("Next → Map Capabilities"):
    next_page("pages/5_Map_Capabilities.py")
