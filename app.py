# app.py (updated)
from flask import Flask, request, jsonify
import PyPDF2
import docx2txt
import os
from analyze import analyze_resume

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# optional home
@app.route('/')
def home():
    return "Resume Parser API Running"

def extract_text_from_file(filepath):
    text = ""
    if filepath.lower().endswith('.pdf'):
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ''
    elif filepath.lower().endswith('.docx'):
        text = docx2txt.process(filepath)
    return text

@app.route('/upload', methods=['POST'])
def upload_file():
    # file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # optional job description field
    jd = request.form.get('job_description', '')  # if frontend posts job_description field

    # extract text
    text = extract_text_from_file(filepath)
    text = text.replace('\n',' ').strip()

    # analyze (this may load BERT model on first call)
    result, _ = analyze_resume(text, jd, skills_path=None, bert_model=None)
    return jsonify(result)

# separate analyze endpoint (accept resume text + jd)
@app.route('/analyze', methods=['POST'])
def analyze_endpoint():
    data = request.get_json(force=True)
    resume_text = data.get('resume_text','')
    jd_text = data.get('job_description','')
    result, _ = analyze_resume(resume_text, jd_text, skills_path=None, bert_model=None)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
