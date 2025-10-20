from flask import Flask, request, jsonify
import spacy
import re
import docx2txt
from PyPDF2 import PdfReader
import tempfile
import os

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Helper — Extract text from DOCX or PDF
def extract_text_from_file(file_path):
    text = ""
    if file_path.endswith(".docx"):
        text = docx2txt.process(file_path)
    elif file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


# ----------- ENTITY EXTRACTION -----------

def extract_entities(text):
    doc = nlp(text)

    # Name extraction
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    # Email extraction
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

    # Phone number extraction
    phones = re.findall(r"\+?\d[\d\- ]{8,}\d", text)

    return {"names": names, "emails": emails, "phones": phones}


# ----------- EDUCATION EXTRACTION -----------

def extract_education(text):
    education_keywords = [
        "bachelor", "master", "phd", "associate", "degree", "diploma",
        "bsc", "msc", "mba", "bachelor of science", "bachelor of arts",
        "university", "college", "institute", "school"
    ]

    education = []
    for line in text.split("\n"):
        for word in education_keywords:
            if word.lower() in line.lower():
                education.append(line.strip())
                break
    return list(set(education))  # remove duplicates


# ----------- SKILLS EXTRACTION -----------

def extract_skills(text):
    # Basic skill keywords list
    skills_list = [
        "python", "java", "c++", "sql", "html", "css", "javascript",
        "machine learning", "deep learning", "data analysis", "excel",
        "flask", "django", "power bi", "tableau", "react", "ai"
    ]

    found_skills = []
    for skill in skills_list:
        if re.search(r"\b" + re.escape(skill) + r"\b", text, re.IGNORECASE):
            found_skills.append(skill.title())

    return found_skills


# ----------- MAIN ROUTE -----------

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        file.save(temp_file.name)
        extracted_text = extract_text_from_file(temp_file.name)
    
    os.remove(temp_file.name)

    # Extract data
    entities = extract_entities(extracted_text)
    education = extract_education(extracted_text)
    skills = extract_skills(extracted_text)

    result = {
        "entities": entities,
        "education": education,
        "skills": skills
    }

    return jsonify(result)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Resume Screening API ready. Upload a DOCX or PDF to /upload"})


if __name__ == "__main__":
    app.run(debug=True)
