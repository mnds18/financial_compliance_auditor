import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from src.langchain_agents import agent
import tempfile

# Set page config
st.set_page_config(page_title="Compliance Auditor - TrustBank AI", layout="wide")

# Load logo
st.sidebar.image("assets/bank_logo.png", width=160)
st.sidebar.title("TrustBank AI")
st.sidebar.markdown("**Compliance & Risk Intelligence**")
st.sidebar.markdown("---")
st.sidebar.info("🔍 Upload a client document to begin a compliance audit powered by GPT + LangChain + RAG.")

# Main title
st.markdown(
    "<h1 style='color:#004080; font-size: 40px;'>📄 Financial Compliance Auditor, developed by Mrig</h1>",
    unsafe_allow_html=True
)

st.markdown("""
<div style='font-size:17px; color:#333; margin-bottom:30px;'>
This internal application automates client document reviews and checks them against TrustBank AI's internal compliance policy documents.
It leverages GPT + RAG + Computer Vision to streamline compliance verification.
</div>
""", unsafe_allow_html=True)

# Upload area
st.markdown("### 📤 Upload Client Document")
uploaded_file = st.file_uploader("Upload a .txt version of the client’s scanned application", type=["txt"])

if uploaded_file:
    document_text = uploaded_file.read().decode('utf-8')
    st.markdown("### 🧾 Document Preview")
    with st.expander("Click to view document content", expanded=True):
        st.code(document_text[:2000], language="text")

    st.markdown("### 🧠 Run Compliance Intelligence Audit")
    if st.button("🚀 Run Audit Now", type="primary"):
        with st.spinner("🔍 Auditing document using GPT agents..."):
            final_output = agent.run(
                f"Extract client information from this document and check compliance:\n{document_text}"
            )
        st.success("✅ Audit completed successfully!")

        st.markdown("### 📝 Final Audit Report")
        st.text_area("Report", final_output, height=350)

        def generate_report(text):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as f:
                f.write(text)
                return f.name

        report_path = generate_report(final_output)

        with open(report_path, "rb") as file:
            st.download_button(
                label="📥 Download Full Audit Report",
                data=file,
                file_name="compliance_audit_report.txt",
                mime="text/plain"
            )
else:
    st.info("📎 Please upload a client document to begin.")
