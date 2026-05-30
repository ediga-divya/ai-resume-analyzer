import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

st.title("AI Resume Analyzer")
st.write("Analyze resumes for ATS keywords, technical skills, and role alignment.")

ROLE_KEYWORDS = {
    "Software Engineer": [
        "python", "java", "javascript", "sql", "data structures", "algorithms",
        "rest api", "backend", "distributed systems", "cloud", "aws", "git"
    ],
    "Data Engineer": [
        "python", "sql", "etl", "airflow", "aws", "redshift", "data pipeline",
        "data warehouse", "spark", "schema design", "data modeling"
    ],
    "AI / ML Engineer": [
        "python", "machine learning", "pytorch", "tensorflow", "nlp",
        "model training", "data preprocessing", "feature engineering",
        "ml pipeline", "inference", "ai infrastructure"
    ]
}

def clean_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()

def analyze_resume(resume_text, selected_role):
    cleaned = clean_text(resume_text)
    keywords = ROLE_KEYWORDS[selected_role]

    matched = []
    missing = []

    for keyword in keywords:
        if keyword.lower() in cleaned:
            matched.append(keyword)
        else:
            missing.append(keyword)

    score = int((len(matched) / len(keywords)) * 100)

    return score, matched, missing

selected_role = st.selectbox(
    "Choose target role",
    ["Software Engineer", "Data Engineer", "AI / ML Engineer"]
)

resume_text = st.text_area(
    "Paste your resume text here",
    height=300,
    placeholder="Paste resume text..."
)

if st.button("Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please paste resume text first.")
    else:
        score, matched, missing = analyze_resume(resume_text, selected_role)

        st.subheader("ATS Match Score")
        st.progress(score)
        st.write(f"**Score:** {score}%")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Matched Keywords")
            if matched:
                for item in matched:
                    st.success(item)
            else:
                st.info("No matched keywords found.")

        with col2:
            st.subheader("Missing Keywords")
            if missing:
                for item in missing:
                    st.error(item)
            else:
                st.success("No important keywords missing.")

        st.subheader("Recommendation")
        if score >= 75:
            st.success("Strong match. Your resume is well aligned with this role.")
        elif score >= 50:
            st.warning("Moderate match. Add more role-specific keywords naturally.")
        else:
            st.error("Low match. Customize your resume more for this role.")
