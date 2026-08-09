# AI Resume Analyzer

## Overview

AI Resume Analyzer is a machine learning-powered Applicant Tracking System (ATS) resume matching application that evaluates how well a resume aligns with a given job description.

The system uses Natural Language Processing (NLP), TF-IDF vectorization, feature engineering, and a Ridge Regression model to predict a resume-job match score. Users can upload resumes in PDF, DOCX, or TXT format and receive an ATS-style compatibility score along with suitability feedback.

The project consists of:

* A machine learning training pipeline developed in Jupyter Notebook
* A trained prediction model serialized using Pickle
* A Streamlit web application for real-time resume analysis

---

## Features

* Resume upload support

  * PDF (.pdf)
  * Microsoft Word (.docx)
  * Text files (.txt)

* Automated text extraction from uploaded resumes

* NLP-based preprocessing

  * Lowercasing
  * Stopword removal
  * Stemming
  * Text normalization

* TF-IDF vectorization with unigram and bigram features

* Skill overlap feature engineering

* Machine learning-based ATS score prediction

* Interactive web interface using Streamlit

* Instant resume-job compatibility assessment

---

## Project Structure

```text
AI_Resume_Analyzer/
│
├── AI_resume_analyzer.ipynb      # Model training pipeline
├── app.py                        # Streamlit application
├── model.pkl                     # Trained Ridge Regression model
├── vectorizer.pkl                # Trained TF-IDF vectorizer
├── resume_data.csv               # Training dataset
├── requirements.txt             # Project dependencies
├── .gitignore
└── README.md
```

---

## Dataset

The model was trained on a dataset containing:

* 9,544 resume-job matching records
* Resume information

  * Career objectives
  * Skills
  * Degrees
  * Educational background
  * Professional experience
* Job information

  * Position titles
  * Required skills
  * Educational requirements
* Match scores representing resume-job compatibility

After preprocessing, relevant textual features were combined to create training samples for machine learning.

---

## Machine Learning Pipeline

### 1. Data Preprocessing

Missing values are handled for key textual fields.

Text preprocessing includes:

* Lowercasing
* Removal of special characters
* Stopword removal using NLTK
* Porter stemming

### 2. Feature Engineering

Two primary feature groups are used:

#### TF-IDF Features

```python
TfidfVectorizer(
    max_features=6000,
    ngram_range=(1, 2),
    stop_words="english"
)
```

#### Skill Overlap Score

A custom similarity metric measures overlap between resume skills and job requirements.

```python
overlap = len(common_skills) / (len(job_skills) + 1)
```

### 3. Model Training

Algorithm:

```text
Ridge Regression
```

Training split:

```text
80% Training
20% Testing
```

### 4. Model Evaluation

Performance metrics achieved:

| Metric                         | Value |
| ------------------------------ | ----- |
| Mean Absolute Error (MAE)      | 0.087 |
| Root Mean Squared Error (RMSE) | 0.113 |

Example prediction:

```text
76.57% ATS Match Score
```

---

## Application Workflow

1. User uploads a resume.
2. Resume text is extracted.
3. User pastes a job description.
4. Text is cleaned and processed.
5. TF-IDF features are generated.
6. Skill overlap is calculated.
7. Features are passed to the trained model.
8. ATS compatibility score is displayed.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### Create Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will launch locally in your browser.

---

## Requirements

```text
streamlit
pandas
numpy
scikit-learn
scipy
nltk
pdfplumber
python-docx
```

---

## Model Files

The application requires the following trained artifacts:

```text
model.pkl
vectorizer.pkl
```

These files contain:

* Trained Ridge Regression model
* Trained TF-IDF vectorizer

Without these files, the application cannot perform predictions.

---

## Supported Resume Formats

| Format | Supported |
| ------ | --------- |
| PDF    | Yes       |
| DOCX   | Yes       |
| TXT    | Yes       |

---

## Future Improvements

Potential enhancements include:

* Resume keyword recommendations
* Skill gap analysis
* Job recommendation engine
* Semantic embeddings using BERT
* Deep learning-based matching models
* Resume ranking for recruiters
* Multi-language resume support
* ATS optimization suggestions
* Explainable AI for score interpretation

---

## Technologies Used

* Python
* Streamlit
* Scikit-learn
* NLTK
* Pandas
* NumPy
* SciPy
* PDFPlumber
* Python-Docx
* Pickle

---

## Live URL

https://ai-based-resume-job-matcher.streamlit.app/

---

## License

This project is licensed under the MIT License.

---

## Author

Developed as a machine learning and NLP project for automated resume screening and ATS score prediction by Wajiha Waqar.
