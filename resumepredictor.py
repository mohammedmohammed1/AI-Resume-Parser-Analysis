import streamlit as st
import pandas as pd
import os
import fitz  # PyMuPDF
import sqlite3
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

st.set_page_config(page_title="📄 Resume Job Role Predictor")

# -------- Training Model --------
@st.cache_resource
def train_model():
    data = {
        'resume': [
            'Experienced in Python, machine learning, and deep learning.',
            'Skilled in SQL, data analysis, and data visualization.',
            'Strong understanding of Java, Spring Boot, and REST APIs.',
            'Expert in social media, brand management, and digital marketing.',
            'Experience in employee onboarding, payroll, and recruitment.',
            'Proficient in Excel, financial reporting, and budgeting.'
        ],
        'role': [
            'ML Engineer',
            'Data Scientist',
            'Data Analyst',
            'Backend Developer',
            'Digital Marketer',
            'HR Executive',
            'Finance Analyst'
        ]
    }
    df = pd.DataFrame(data)
    model = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression())
    ])
    model.fit(df['resume'], df['role'])
    return model

model = train_model()

# -------- Read Text from File --------
def extract_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    elif file.name.endswith(".docx"):
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        st.error("Unsupported file format.")
    return text

# -------- Extract Candidate Name --------
def extract_candidate_name(text):
    lines = text.strip().split('\n')
    for line in lines:
        if line.strip():
            return line.strip()
    return "Unknown"

# -------- Extract Skills (Simple Matching) --------
def extract_skills(text):
    skills = ['python', 'java', 'sql', 'excel', 'machine learning', 'deep learning',
              'recruitment', 'budgeting', 'digital marketing', 'brand management',
              'spring boot', 'data visualization', 'financial reporting']
    found_skills = [skill for skill in skills if skill.lower() in text.lower()]
    return ', '.join(found_skills) if found_skills else "Not Found"

# -------- Database Setup --------
def setup_database():
    db_path = "resume_predictions.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS resume_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            predicted_role TEXT,
            extracted_skills TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    return conn

# -------- Save to Database --------
def save_prediction_to_db(conn, name, role, skills, status):
    c = conn.cursor()
    c.execute("INSERT INTO resume_predictions (candidate_name, predicted_role, extracted_skills, status) VALUES (?, ?, ?, ?)",
              (name, role, skills, status))
    conn.commit()

# -------- Main App UI --------
st.title("📄 Resume Job Role Predictor")

uploaded_file = st.file_uploader("Upload a Resume (.pdf or .docx)", type=["pdf", "docx"])

if uploaded_file:
    resume_text = extract_text(uploaded_file)
    st.subheader("🔍 Resume Preview")
    st.text_area("Text from Resume", resume_text, height=250)

    candidate_name = extract_candidate_name(resume_text)
    predicted_role = model.predict([resume_text])[0]
    extracted_skills = extract_skills(resume_text)

    applicable_roles = ['ML Engineer', 'Data Analyst', 'Backend Developer', 'Digital Marketer', 'HR Executive', 'Finance Analyst']
    status = "Match" if predicted_role in applicable_roles else "Not Match"
    message = (
        f"✅ Predicted Role: **{predicted_role}**\n\nAll the best for your career!"
        if status == "Match"
        else "❌ Unfortunately your profile is not applicable for this role. Thank you for your interest."
    )

    # Save prediction to database
    conn = setup_database()
    save_prediction_to_db(conn, candidate_name, predicted_role, extracted_skills, status)
    conn.close()

    st.subheader("📝 Candidate Summary")
    st.write(f"**Candidate Name:** {candidate_name}")
    st.write(f"**Predicted Role:** {predicted_role}")
    st.write(f"**Extracted Skills:** {extracted_skills}")

    if status == "Match":
        st.success(message)
    else:
        st.error(message)

    # Display recent entries
    conn = sqlite3.connect("resume_predictions.db")
    df = pd.read_sql_query(
        "SELECT candidate_name, predicted_role, extracted_skills, status FROM resume_predictions ORDER BY id DESC LIMIT 10",
        conn)
    st.subheader("📊 Recent Predictions")
    st.dataframe(df)
    conn.close()
