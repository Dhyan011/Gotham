def compute_risk_score(prior_offenses, severity_avg, days_since_last_crime, distinct_districts):
    """
    4-component risk scoring:
    - prior_offenses 40% (maxes out at 10)
    - severity_avg 30% (scale 1-10)
    - recency 20% (maxes out at 365 days, inverse)
    - geographic_spread 10% (maxes out at 5 districts)
    """
    
    # Normalize prior offenses (0-1)
    c1 = min(prior_offenses / 10.0, 1.0)
    
    # Normalize severity (0-1)
    c2 = min(severity_avg / 10.0, 1.0)
    
    # Normalize recency (0-1)
    c3 = max(0, 1.0 - (days_since_last_crime / 365.0))
    
    # Normalize geographic spread (0-1)
    c4 = min(distinct_districts / 5.0, 1.0)
    
    score = (c1 * 0.4) + (c2 * 0.3) + (c3 * 0.2) + (c4 * 0.1)
    
    # Scale to 10
    final_score = round(score * 10, 2)
    
    if final_score > 7.5:
        label = "High"
    elif final_score > 4.0:
        label = "Medium"
    else:
        label = "Low"
        
    return {
        "risk_score": final_score,
        "risk_label": label,
        "breakdown": {
            "prior_offenses_weight": round(c1 * 0.4 * 10, 2),
            "severity_avg_weight": round(c2 * 0.3 * 10, 2),
            "recency_weight": round(c3 * 0.2 * 10, 2),
            "geographic_spread_weight": round(c4 * 0.1 * 10, 2)
        }
    }

if __name__ == "__main__":
    pass
