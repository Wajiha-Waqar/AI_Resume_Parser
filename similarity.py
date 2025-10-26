# similarity.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def tfidf_similarity(text1, text2):
    docs = [text1 or "", text2 or ""]
    vect = TfidfVectorizer(ngram_range=(1,2), stop_words='english', max_features=5000)
    X = vect.fit_transform(docs)
    cos = cosine_similarity(X[0], X[1])[0][0]
    return float(cos)

# BERT (sentence-transformers)
def bert_similarity(text1, text2, model=None):
    try:
        from sentence_transformers import SentenceTransformer
        if model is None:
            model = SentenceTransformer('all-MiniLM-L6-v2')
        emb1 = model.encode(text1 or "", convert_to_numpy=True)
        emb2 = model.encode(text2 or "", convert_to_numpy=True)
        denom = np.linalg.norm(emb1)*np.linalg.norm(emb2)
        if denom == 0:
            return 0.0, model
        cos = float(np.dot(emb1, emb2) / denom)
        return cos, model
    except Exception as e:
        print("BERT error:", e)
        return None, model
