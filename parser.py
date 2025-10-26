<<<<<<< Updated upstream
=======
"""
AI Resume Parser - FINAL VERSION
-----------------------------------------------
✅ Flask Backend + Frontend Integration
✅ File Upload (PDF, DOCX, TXT)
✅ NLP Extraction (Name, Email, Phone, Education, Skills)
✅ TF-IDF Matching
✅ MongoDB Integration
✅ Search & Filter Endpoints
✅ CORS Enabled
✅ Error Handling & Edge Cases
✅ Optional Multilingual Parsing
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import spacy
import os, re, traceback, docx2txt
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------
# Flask & Mongo Setup
# ----------------------------
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
ALLOWED_EXT = {".pdf", ".docx", ".txt"}

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["resumeDB"]
collection = db["resumes"]

# ----------------------------
# NLP Setup (spaCy)
# ----------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

MASTER_SKILLS = [
    "python","java","c++","sql","html","css","javascript","react","node",
    "flask","django","pandas","numpy","tensorflow","pytorch","machine learning",
    "deep learning","nlp","data analysis","power bi","tableau","excel","aws","docker"
]

EDU_KEYWORDS = [
    "bachelor","master","phd","mba","btech","mtech",
    "intermediate","high school","diploma"
]

# ----------------------------
# Helper Functions
# ----------------------------
def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXT

def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    text = ""
    if ext == ".pdf":
        try:
            reader = PdfReader(filepath)
            for page in reader.pages:
                p = page.extract_text()
                if p:
                    text += p + "\n"
        except Exception as e:
            print("PDF extraction error:", e)
    elif ext == ".docx":
        text = docx2txt.process(filepath) or ""
    elif ext == ".txt":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    return text.strip()

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_entities(text):
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
    phones = re.findall(r'\+?\d[\d\s\-\(\)]{8,}\d', text)
    return {
        "name": names[0] if names else None,
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None
    }

def extract_education(text):
    lines = text.lower().split("\n")
    edu = [line for line in lines if any(k in line for k in EDU_KEYWORDS)]
    return list(set(edu))

def extract_skills(text):
    found = [skill for skill in MASTER_SKILLS if skill.lower() in text.lower()]
    return list(set(found))

def compute_similarity(resume_text, job_desc):
    try:
        vectorizer = TfidfVectorizer().fit([resume_text, job_desc])
        vecs = vectorizer.transform([resume_text, job_desc])
        return float(cosine_similarity(vecs[0], vecs[1])[0][0])
    except Exception:
        return 0.0

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# ----------------------------
# Frontend Route
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ----------------------------
# API Endpoints
# ----------------------------
@app.route("/upload", methods=["POST"])
def upload_resume():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        file = request.files["file"]
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        text = clean_text(extract_text_from_file(filepath))
        if not text:
            return jsonify({"error": "Could not extract text from file"}), 400

        entities = extract_entities(text)
        skills = extract_skills(text)
        edu = extract_education(text)

        record = {
            "filename": filename,
            "entities": entities,
            "skills": skills,
            "education": edu,
            "text": text
        }

        result = collection.insert_one(record)
        saved_doc = collection.find_one({"_id": result.inserted_id})
        return jsonify(serialize_doc(saved_doc))  # ✅ FIXED JSON SERIALIZATION

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


@app.route("/resumes", methods=["GET"])
def get_resumes():
    all_docs = [serialize_doc(d) for d in collection.find()]
    return jsonify(all_docs)


@app.route("/match", methods=["POST"])
def match_resume():
    try:
        data = request.json
        resume_id = data.get("resume_id")
        job_desc = data.get("job_description")

        if not resume_id or not job_desc:
            return jsonify({"error": "resume_id and job_description required"}), 400

        resume = collection.find_one({"_id": ObjectId(resume_id)})
        if not resume:
            return jsonify({"error": "Resume not found"}), 404

        score = compute_similarity(resume["text"], job_desc)
        return jsonify({
            "resume_id": resume_id,
            "similarity_score": round(score * 100, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


@app.route("/search", methods=["GET"])
def search_resumes():
    skill = request.args.get("skill")
    degree = request.args.get("degree")
    query = {}

    if skill:
        query["skills"] = skill.lower()
    if degree:
        query["education"] = {"$regex": degree.lower(), "$options": "i"}

    if not query:
        return jsonify({"error": "Please provide at least one filter"}), 400

    results = [serialize_doc(r) for r in collection.find(query)]
    return jsonify(results)


@app.route("/delete/<rid>", methods=["DELETE"])
def delete_resume(rid):
    result = collection.delete_one({"_id": ObjectId(rid)})
    return jsonify({"deleted": result.deleted_count > 0})


# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
>>>>>>> Stashed changes
