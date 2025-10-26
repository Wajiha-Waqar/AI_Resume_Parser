# analyze.py
import json
from skill_extractor import extract_skills, load_skills
from similarity import tfidf_similarity, bert_similarity

# analyze resume against JD and return structured response
def analyze_resume(resume_text, jd_text="", skills_path=None, bert_model=None):
    # 1) extract skills
    skills_list = load_skills(skills_path)
    extracted = extract_skills(resume_text, skills_path)

    # 2) JD skills (if provided)
    jd_skills_set = set()
    if jd_text and jd_text.strip():
        jd_extracted = extract_skills(jd_text, skills_path)
        jd_skills_set = set([s['skill'] for s in jd_extracted])

    resume_skills_set = set([s['skill'] for s in extracted])
    matched_skills = list(resume_skills_set.intersection(jd_skills_set))

    # skill match score
    skill_match_score = 0.0
    if jd_skills_set:
        skill_match_score = len(matched_skills) / len(jd_skills_set)
    else:
        skill_match_score = min(len(resume_skills_set)/10.0, 1.0)

    # TF-IDF
    tfidf_sc = None
    if jd_text and jd_text.strip():
        try:
            tfidf_sc = tfidf_similarity(resume_text, jd_text)
        except Exception as e:
            tfidf_sc = 0.0

    # BERT
    bert_sc = None
    if jd_text and jd_text.strip():
        bert_res, bert_model = bert_similarity(resume_text, jd_text, model=bert_model)
        if bert_res is None:
            bert_sc = 0.0
        else:
            # map to 0..1 (just in case)
            bert_sc = (bert_res + 1.0)/2.0 if bert_res < 0 or bert_res > 1 else bert_res

    # combine weights
    w_skill = 0.5
    w_tfidf = 0.25
    w_bert = 0.25

    tfidf_val = tfidf_sc if tfidf_sc is not None else 0.0
    bert_val = bert_sc if bert_sc is not None else 0.0

    job_fit = w_skill*skill_match_score + w_tfidf*tfidf_val + w_bert*bert_val
    job_fit_percent = round(job_fit * 100, 2)

    response = {
        "summary": {
            "job_fit_percent": job_fit_percent,
            "skill_match_score": round(skill_match_score, 3),
            "tfidf_score": round(tfidf_val, 3),
            "bert_score": round(bert_val, 3)
        },
        "extracted_skills": extracted,
        "matched_skills": matched_skills,
        "jd_skills": list(jd_skills_set),
        "notes": "weights -> skill:50%, tfidf:25%, bert:25%"
    }
    return response, bert_model

# quick test
if __name__ == "__main__":
    r = "Python, Flask, Docker, Pandas"
    jd = "Looking for Python developer with Flask and Docker experience"
    print(json.dumps(analyze_resume(r, jd)[0], indent=2))
