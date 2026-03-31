import streamlit as st
import requests

# ---- Page config ----
st.set_page_config(
    page_title="Research Paper AI Assistant",
    page_icon="🧠",
    layout="centered"
)

# ---- Header ----
st.title("🧠 Research Paper AI Assistant")
st.markdown("Upload any research paper and ask questions about it in plain English.")
st.divider()

# ---- Session state for chat history ----
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

# ---- PDF Upload Section ----
st.subheader("📄 Step 1 — Upload your research paper")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
    help="Upload any research paper in PDF format"
)

if uploaded_file is not None and not st.session_state.pdf_uploaded:
    with st.spinner("Processing your PDF... this may take a minute ⏳"):
        # Send PDF to FastAPI backend
        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        )

        if response.status_code == 200:
            data = response.json()
            st.success(f"✅ PDF processed! {data['chunks_stored']} chunks stored.")
            st.session_state.pdf_uploaded = True
            st.session_state.messages = []  # reset chat on new upload
        else:
            st.error("❌ Failed to process PDF. Make sure the backend is running.")

# ---- Reset button ----
if st.session_state.pdf_uploaded:
    if st.button("📤 Upload a different PDF"):
        st.session_state.pdf_uploaded = False
        st.session_state.messages = []
        st.rerun()

st.divider()

# ---- Q&A Section ----
st.subheader("💬 Step 2 — Ask questions about the paper")

if not st.session_state.pdf_uploaded:
    st.info("👆 Please upload a PDF first to start asking questions.")
else:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if question := st.chat_input("Ask anything about the paper..."):
        # Show user message
        with st.chat_message("user"):
            st.markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})

        # Get answer from backend
        with st.chat_message("assistant"):
            with st.spinner("Thinking... 🤔"):
                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={"question": question}
                )

                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.markdown(answer)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                else:
                    st.error("❌ Failed to get answer. Try again.")