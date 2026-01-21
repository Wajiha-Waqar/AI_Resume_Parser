# 📄 ATS Resume & Job Matching System

An AI-powered Applicant Tracking System (ATS) that matches resumes with job descriptions using NLP and Machine Learning.

## 🚀 Features
- Upload resumes in **PDF, DOCX, TXT**
- Paste job descriptions
- TF-IDF + Skill Overlap based matching
- Ridge Regression ML model
- ATS compatibility score (%)
- Streamlit web interface

## 🧠 Tech Stack
- Python
- Streamlit
- Scikit-learn
- NLP (NLTK, TF-IDF)
- PDF & DOCX parsing

## 📂 Project Structure
ats-resume-matcher/
│── app.py
│── model.pkl
│── vectorizer.pkl
│── requirements.txt
│── README.md

## ▶️ How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
