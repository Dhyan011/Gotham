from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import CaseMaster, Unit

def compute_similar_cases(db: Session, target_fir_id: int):
    target_case = db.query(CaseMaster, Unit).join(Unit).filter(CaseMaster.fir_id == target_fir_id).first()
    if not target_case:
        return []
        
    t_case, t_unit = target_case
    all_cases = db.query(CaseMaster, Unit).join(Unit).filter(CaseMaster.fir_id != target_fir_id).all()
    
    if not all_cases:
        return []
        
    corpus = [t_case.brief_facts or ""]
    case_ids = []
    for c, u in all_cases:
        corpus.append(c.brief_facts or "")
        case_ids.append((c, u))
        
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    except ValueError:
        cosine_sim = [0] * len(all_cases)
        
    results = []
    for i, (c, u) in enumerate(case_ids):
        base_score = cosine_sim[i]
        
        # Bonuses
        if c.crime_type == t_case.crime_type:
            base_score += 0.2
        if u.district == t_unit.district:
            base_score += 0.1
            
        if c.date_of_occurrence and t_case.date_of_occurrence:
            date_diff = abs((c.date_of_occurrence - t_case.date_of_occurrence).days)
            if date_diff <= 30:
                base_score += 0.1
                
        results.append({
            "fir_id": c.fir_id,
            "fir_number": c.fir_number,
            "similarity_score": round(min(base_score, 1.0), 2)
        })
        
    # Sort and return top 10
    results.sort(key=lambda x: x['similarity_score'], reverse=True)
    return results[:10]

if __name__ == "__main__":
    pass
