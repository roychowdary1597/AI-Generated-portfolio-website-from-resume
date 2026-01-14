# AI-Generated Portfolio Website from Resume

An end-to-end **AI-powered application** that converts a resume (PDF or DOCX) into a **production-ready, FAANG-style portfolio website**.  
The system automates document parsing, prompt engineering, frontend code generation, and deployment using **Streamlit and LangChain**.

## 🚀 AI Mentor Chatbot – Demo

## Project Demo

[![Watch the demo video](assets/thumbnail.png)](https://github.com/roychowdary1597/AI-Generated-portfolio-website-from-resume/compressed-video.mp4)

*Click the image to play the demo video.*



---

## 📌 Overview

Creating a portfolio website usually requires frontend skills and design experience.  
This project removes that barrier by allowing users to upload a resume and instantly receive a **complete, responsive website** built with **HTML, CSS, and JavaScript**.

**Pipeline:**  
Resume → Structured Website Prompt → Website Source Code

---

## 🚀 Features

- Upload **PDF or DOCX** resumes  
- Automatic extraction of:
  - Name
  - Skills
  - Experience
  - Projects
  - Education
- **Two-stage LLM pipeline**:
  1. Resume → Structured website specification  
  2. Specification → HTML / CSS / JavaScript  
- FAANG-style, mobile-responsive design  
- ZIP download of deployable website files  
- Secure API key handling using Streamlit Secrets  

---
## 🧠 System Architecture

Resume Upload (PDF / DOCX)
↓
Text Extraction (PyPDF2 / python-docx)
↓
LLM #1 (Resume → Website Prompt)
↓
LLM #2 (Prompt → HTML / CSS / JS)
↓
Streamlit UI + ZIP Export


---

## 🛠️ Technology Stack

| Layer | Tools |
|------|------|
| UI | Streamlit |
| Backend | Python |
| Resume Parsing | PyPDF2, python-docx |
| LLM Orchestration | LangChain |
| LLM Provider | Google Gemini |
| Frontend Output | HTML, CSS, JavaScript |
| Packaging | zipfile |

---

## 📂 Project Structure

.
├── main.py
├── requirements.txt
├── .gitignore
├── README.md


> `.env` is excluded from GitHub for security reasons.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


