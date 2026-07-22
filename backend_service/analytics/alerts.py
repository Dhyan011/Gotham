import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import CaseMaster, Unit

def get_alerts(db: Session):
    cases = db.query(CaseMaster.date_of_occurrence, CaseMaster.crime_type, Unit.district).join(Unit, CaseMaster.unit_id == Unit.unit_id).all()
    if not cases:
        return []
        
    df = pd.DataFrame(cases, columns=['date', 'crime_type', 'district'])
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    
    monthly_counts = df.groupby(['district', 'crime_type', 'month']).size().reset_index(name='count')
    alerts = []
    
    for (district, crime_type), group in monthly_counts.groupby(['district', 'crime_type']):
        group = group.sort_values('month')
        if len(group) < 2:
            continue
            
        current_count = group.iloc[-1]['count']
        history = group.iloc[:-1]
        
        # 6-month rolling mean
        recent_history = history.tail(6)
        mean = recent_history['count'].mean()
        std = recent_history['count'].std()
        
        if std and std > 0:
            z_score = (current_count - mean) / std
            if z_score > 2.0:
                alerts.append({
                    "district": district,
                    "crime_type": crime_type,
                    "z_score": round(z_score, 2),
                    "current_count": current_count,
                    "mean_6m": round(mean, 2)
                })
    
    return alerts

if __name__ == "__main__":
    pass
