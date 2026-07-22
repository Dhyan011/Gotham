import Levenshtein
import re

def trigram_similarity(s1, s2):
    def get_trigrams(s):
        s = f"  {s}  "
        return set([s[i:i+3] for i in range(len(s)-2)])
        
    t1 = get_trigrams(s1.lower())
    t2 = get_trigrams(s2.lower())
    
    if not t1 or not t2:
        return 0.0
    return len(t1.intersection(t2)) / float(len(t1.union(t2)))

def fuzzy_name_match(name1, name2):
    lev_dist = Levenshtein.distance(name1.lower(), name2.lower())
    max_len = max(len(name1), len(name2))
    lev_sim = 1 - (lev_dist / max_len) if max_len > 0 else 0.0
    
    tri_sim = trigram_similarity(name1, name2)
    return (lev_sim * 0.6) + (tri_sim * 0.4)

def evidence_fusion(m1, m2):
    """
    Dempster-Shafer evidence fusion for two masses.
    m1, m2: dict of {hypothesis: probability, ...}
    Includes 'match', 'no_match', 'uncertain'
    """
    K = m1.get('match', 0)*m2.get('no_match', 0) + m1.get('no_match', 0)*m2.get('match', 0)
    if K == 1:
        return {'match': 0, 'no_match': 0, 'uncertain': 1}
        
    fused = {}
    fused['match'] = (m1.get('match', 0)*m2.get('match', 0) + m1.get('match', 0)*m2.get('uncertain', 0) + m1.get('uncertain', 0)*m2.get('match', 0)) / (1 - K)
    fused['no_match'] = (m1.get('no_match', 0)*m2.get('no_match', 0) + m1.get('no_match', 0)*m2.get('uncertain', 0) + m1.get('uncertain', 0)*m2.get('no_match', 0)) / (1 - K)
    fused['uncertain'] = (m1.get('uncertain', 0)*m2.get('uncertain', 0)) / (1 - K)
    
    return fused

def resolve_entities(entity_a, entity_b):
    # Name evidence
    name_sim = fuzzy_name_match(entity_a.get('name', ''), entity_b.get('name', ''))
    m_name = {'match': name_sim * 0.8, 'no_match': (1-name_sim)*0.8, 'uncertain': 0.2}
    
    # Descriptor evidence
    desc_a = entity_a.get('descriptor', {})
    desc_b = entity_b.get('descriptor', {})
    if desc_a and desc_b and abs(desc_a.get('height_cm', 0) - desc_b.get('height_cm', 0)) <= 5:
        m_desc = {'match': 0.7, 'no_match': 0.1, 'uncertain': 0.2}
    else:
        m_desc = {'match': 0.1, 'no_match': 0.7, 'uncertain': 0.2}
        
    fused = evidence_fusion(m_name, m_desc)
    return fused

if __name__ == "__main__":
    pass
