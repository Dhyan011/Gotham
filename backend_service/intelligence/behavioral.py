import numpy as np
from collections import defaultdict

def extract_crime_sequence(crimes):
    crimes = sorted(crimes, key=lambda x: x['date'])
    return [c['crime_type'] for c in crimes]

def compute_escalation_slope(crimes):
    if len(crimes) < 2:
        return 0.0
    crimes = sorted(crimes, key=lambda x: x['date'])
    severities = [c['severity_weight'] for c in crimes]
    x = np.arange(len(severities))
    slope, _ = np.polyfit(x, severities, 1)
    return slope

def markov_chain_prediction(sequence, all_sequences):
    transitions = defaultdict(lambda: defaultdict(int))
    for seq in all_sequences:
        for i in range(len(seq)-1):
            transitions[seq[i]][seq[i+1]] += 1
            
    if not sequence:
        return None
        
    last_crime = sequence[-1]
    if last_crime not in transitions or not transitions[last_crime]:
        return None
        
    next_crimes = transitions[last_crime]
    total = sum(next_crimes.values())
    probs = {k: v/total for k, v in next_crimes.items()}
    return max(probs.items(), key=lambda x: x[1])

def detect_mo_drift(old_tags, new_tags):
    old_set = set(old_tags)
    new_set = set(new_tags)
    if not old_set and not new_set:
        return 0.0
    intersection = len(old_set.intersection(new_set))
    union = len(old_set.union(new_set))
    jaccard = intersection / union
    return 1.0 - jaccard # Drift is opposite of similarity

if __name__ == "__main__":
    pass
