# skill_extractor.py
import re
from rapidfuzz import fuzz

def load_skills(path=None):
    if path:
        import csv
        skills=[]
        with open(path,encoding='utf-8') as f:
            reader=csv.DictReader(f)
            for row in reader:
                skills.append(row['skill'].lower())
        return skills
    # fallback list (expand as needed)
    return ["python","c++","java","sql","flask","django","react","node.js","tensorflow","pandas","numpy","git","docker","kubernetes","machine learning","data analysis","aws","azure","html","css","javascript"]

def normalize(text):
    text = (text or "").lower()
    text = re.sub(r'[\r\n]+', ' ', text)
    text = re.sub(r'[^a-z0-9\.\+\s\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_skills_from_text(text, skills_list, fuzzy_threshold=80):
    text_norm = normalize(text)
    found = {}
    # exact matches
    for skill in skills_list:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_norm):
            found[skill] = {'match_type': 'exact', 'score': 100}
    # fuzzy for remaining
    remaining = [s for s in skills_list if s not in found]
    for s in remaining:
        score = fuzz.partial_ratio(s.lower(), text_norm)
        if score >= fuzzy_threshold:
            found[s] = {'match_type': 'fuzzy', 'score': int(score)}
    # format
    result = []
    for k,v in sorted(found.items(), key=lambda x: x[1]['score'], reverse=True):
        result.append({'skill': k, 'match_type': v['match_type'], 'score': v['score']})
    return result

def extract_skills(text, skills_path=None):
    skills_list = load_skills(skills_path)
    # try detect a skills section quickly (heuristic)
    skills_section = ""
    m = re.search(r'(skills|technical skills|skillset)(:|\n)', text or "", flags=re.I)
    if m:
        start = m.end()
        skills_section = (text or "")[start:start+800]
    # higher sensitivity in skills section
    found = {}
    if skills_section:
        sec = extract_skills_from_text(skills_section, skills_list, fuzzy_threshold=70)
        for s in sec:
            found[s['skill']] = {'match_type': s['match_type'], 'score': s['score'], 'weight': 1.2}
    full = extract_skills_from_text(text, skills_list, fuzzy_threshold=80)
    for s in full:
        if s['skill'] in found:
            found[s['skill']]['score'] = max(found[s['skill']]['score'], s['score'])
        else:
            found[s['skill']] = {'match_type': s['match_type'], 'score': s['score'], 'weight': 1.0}
    # build list
    out = []
    for k,v in found.items():
        out.append({'skill': k, 'match_type': v['match_type'], 'score': v['score'], 'weight': v['weight']})
    out.sort(key=lambda x: x['score']*x['weight'], reverse=True)
    return out

# quick test
if __name__ == "__main__":
    s = "Experienced Python developer with Flask, Docker, and some AWS. Familiar with numpy and pandas."
    print(extract_skills(s))
