import pandas as pd
import os

DATASET_PATH = "/Users/dhyanpatel/Desktop/Gotham/dataset/Karnataka Crime Data Dec 2025.csv"

def get_anomaly_data():
    """
    Parses Dec 2025 crime data to calculate current vs previous month/year anomalies.
    """
    if not os.path.exists(DATASET_PATH):
        print(f"File not found: {DATASET_PATH}")
        return []

    try:
        df = pd.read_csv(DATASET_PATH)
        df.columns = df.columns.str.strip()
        
        # Clean headers to easy names based on the 764 row file we inspected
        # Columns: 'Sl No', 'Heads of Crime', 'Major Heads', 'Minor Heads', 
        # 'During the current year upto the end of month under review', 
        # 'During the corresponding month of previous year', 
        # 'During the previous month', 'During the current month'
        
        # We focus on rows with valid Major Heads and clean counts
        df = df.dropna(subset=['Major Heads'])
        
        results = []
        for _, row in df.iterrows():
            major_head = str(row['Major Heads']).strip()
            minor_head = str(row['Minor Heads']).strip() if pd.notna(row['Minor Heads']) else ""
            
            def clean_count(val):
                if pd.isna(val): return 0
                val_str = str(val).replace(',', '').strip()
                return int(val_str) if val_str.isdigit() else 0
                
            current_month = clean_count(row.get('During the current month', 0))
            prev_month = clean_count(row.get('During the previous month', 0))
            prev_year_month = clean_count(row.get('During the corresponding month of previous year', 0))
            
            # Simple Statistical Spike Logic: 
            # If current month is > 150% of previous month AND > 5 cases absolute to avoid noise
            is_anomaly = False
            ratio = 0
            if current_month > 5 and prev_month > 0:
                ratio = current_month / prev_month
                if ratio >= 1.5:
                    is_anomaly = True

            # Calculate Trend Indicator (Phase 5)
            # Compare current to average of prev_month and prev_year_month, or simple direction
            trend_val = current_month - prev_month
            trend_direction = "STABLE"
            if trend_val > max(2, prev_month * 0.1): # more than 10% or 2 cases increase
                trend_direction = "UPWARD"
            elif trend_val < -max(2, prev_month * 0.1):
                trend_direction = "DOWNWARD"

            if is_anomaly or trend_direction != "STABLE":
                results.append({
                    "crime_type": f"{major_head} - {minor_head}".strip(" - "),
                    "current": current_month,
                    "previous": prev_month,
                    "previous_year": prev_year_month,
                    "ratio": round(ratio, 1) if prev_month > 0 else 0,
                    "basis": f"Spike detected: {current_month} cases this month vs. {prev_month} last month ({round(ratio, 1)}x)." if is_anomaly else f"Trend monitored: {current_month} vs {prev_month} prev.",
                    "severity": "HIGH" if ratio >= 3.0 else ("MEDIUM" if is_anomaly else "INFO"),
                    "trend": trend_direction,
                    "is_anomaly": is_anomaly
                })
                    
        # Sort by anomaly severity then ratio descending
        results = sorted(results, key=lambda x: (x['is_anomaly'], x['ratio']), reverse=True)
        return results[:10] # Top 10 anomalies
        
    except Exception as e:
        print(f"Error parsing anomaly data: {e}")
        return []

if __name__ == "__main__":
    anomalies = get_anomaly_data()
    for a in anomalies:
        print(a)
