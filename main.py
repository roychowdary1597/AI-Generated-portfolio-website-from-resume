import streamlit as st
import os
import zipfile
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# --------------------------------------------------
# Environment
# --------------------------------------------------
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------
st.set_page_config(
    page_title="AI Resume → Portfolio Generator",
    page_icon="🌐",
    layout="centered"
)

st.title("AI Generated Portfolio Website from Resume")
st.caption("Upload your resume to get a production-ready portfolio website")

# --------------------------------------------------
# Resume Extractors
# --------------------------------------------------
def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_docx_text(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs if p.text)


def extract_block(text, tag):
    marker = f"--{tag}--"
    if marker in text:
        return text.split(marker)[1].split(marker)[0].strip()
    return ""

# --------------------------------------------------
# Upload Resume
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload PDF or DOCX",
    type=["pdf", "docx"]
)

if "generated" not in st.session_state:
    st.session_state.generated = False

if uploaded_file is None:
    st.info("Please upload a resume to continue.")
    st.stop()

# --------------------------------------------------
# Direct Generation After Upload
# --------------------------------------------------
if uploaded_file and not st.session_state.generated:

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        resume_text = extract_pdf_text(uploaded_file)
    elif file_name.endswith(".docx"):
        resume_text = extract_docx_text(uploaded_file)
    else:
        st.error("❌ Upload supported documents only (.pdf or .docx)")
        st.stop()

    st.success("Resume extracted successfully")

    with st.spinner("Generating portfolio website using AI..."):

        # ==================================================
        # LLM #1 — Resume → Structured Prompt
        # ==================================================
        prompt_generator = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.6
        )

        prompt_messages = [
            SystemMessage(
                content="""
You are an expert technical resume analyst.

Convert the resume into a structured website specification.

Extract:
- Name
- Role
- Professional summary
- Skills (grouped)
- Projects (with impact)
- Experience
- Education
- Suggested design style (FAANG-style, minimal)

Output ONLY a structured WEBSITE PROMPT.
Do NOT generate code.
"""
            ),
            HumanMessage(content=resume_text)
        ]

        structured_prompt = prompt_generator.invoke(prompt_messages).content

        if not structured_prompt.strip():
            st.error("Structured prompt generation failed.")
            st.stop()

        # ==================================================
        # LLM #2 — Prompt → Website Code
        # ==================================================
        website_generator = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.6
        )

        website_messages = [
            SystemMessage(
                content="""
You are a senior frontend web developer.

Generate a professional FAANG-style portfolio website.

Rules:
1. Use ONLY HTML, CSS, JavaScript
2. Output ONLY code
3. Use EXACT format:

--html--
[HTML]
--html--

--css--
[CSS]
--css--

--js--
[JS]
--js--

4. HTML MUST include <meta charset="UTF-8">
5. Responsive, clean, production-ready
"""
            ),
            HumanMessage(content=structured_prompt)
        ]

        website_response = website_generator.invoke(website_messages).content

    # --------------------------------------------------
    # Parse Code
    # --------------------------------------------------
    html_code = extract_block(website_response, "html")
    css_code = extract_block(website_response, "css")
    js_code = extract_block(website_response, "js")

    # --------------------------------------------------
    # Write Files (UTF-8 Safe)
    # --------------------------------------------------
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_code)

    with open("style.css", "w", encoding="utf-8") as f:
        f.write(css_code)

    with open("script.js", "w", encoding="utf-8") as f:
        f.write(js_code)

    # --------------------------------------------------
    # ZIP Export
    # --------------------------------------------------
    with zipfile.ZipFile("portfolio_website.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("index.html")
        zipf.write("style.css")
        zipf.write("script.js")

    st.session_state.generated = True

    with open("portfolio_website.zip", "rb") as f:
        st.download_button(
            "Download Portfolio Website",
            data=f,
            file_name="portfolio_website.zip",
            mime="application/zip"
        )

    st.success("Portfolio website generated successfully")
