import pandas as pd
import os

DATASET_PATH = "/Users/dhyanpatel/Desktop/Gotham/dataset/Karnataka Crime Data 2025 (1).csv"

# Approximate coordinates for major Karnataka police units/districts for mapping
DISTRICT_COORDS = {
    "Bengaluru City": {"lat": 12.9716, "lng": 77.5946},
    "Mysuru City": {"lat": 12.2958, "lng": 76.6394},
    "Hubballi Dharwad City": {"lat": 15.3647, "lng": 75.1240},
    "Mangaluru City": {"lat": 12.9141, "lng": 74.8560},
    "Belagavi City": {"lat": 15.8497, "lng": 74.4977},
    "Kalaburagi City": {"lat": 17.3297, "lng": 76.8343},
    "Tumakuru": {"lat": 13.3409, "lng": 77.1005},
    "Dakshina Kannada": {"lat": 12.8647, "lng": 75.1517},
    "Udupi": {"lat": 13.3409, "lng": 74.7421},
    "Shivamogga": {"lat": 13.9299, "lng": 75.5681},
    "Hassan": {"lat": 13.0033, "lng": 76.1004},
    "Mandya": {"lat": 12.5222, "lng": 76.8943},
    "Bengaluru Dist": {"lat": 13.1986, "lng": 77.6256},
    "Kolar": {"lat": 13.1367, "lng": 78.1291},
    # Default for missing/smaller units for visual scatter
    "DEFAULT": {"lat": 14.5, "lng": 76.0}
}

def get_district_map_data():
    """
    Parses the real dataset to return district-level crime volumes and coordinates.
    """
    if not os.path.exists(DATASET_PATH):
        print(f"File not found: {DATASET_PATH}")
        return []

    try:
        # Load CSV, skipping the first row if it's a sub-header, and dropping fully NA rows
        df = pd.read_csv(DATASET_PATH)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Drop rows where 'Districts/Units' is missing or just header separators
        df = df.dropna(subset=['Districts/Units'])
        df = df[~df['Districts/Units'].isin(['Commissionerates', 'Districts', 'State Total'])]
        
        results = []
        for _, row in df.iterrows():
            district_name = str(row['Districts/Units']).strip()
            
            # Clean counts (handle commas, NaNs)
            def clean_count(val):
                if pd.isna(val): return 0
                val_str = str(val).replace(',', '').strip()
                return int(val_str) if val_str.isdigit() else 0
                
            ipc_count = clean_count(row.get('IPC/BNS Crimes', 0))
            sll_count = clean_count(row.get('SLL Crimes', 0))
            total_crimes = ipc_count + sll_count
            
            if total_crimes == 0:
                continue

            coords = DISTRICT_COORDS.get(district_name, DISTRICT_COORDS["DEFAULT"])
            
            # Add slight jitter for DEFAULT so they don't exactly stack
            lat = coords["lat"]
            lng = coords["lng"]
            if coords == DISTRICT_COORDS["DEFAULT"]:
                import random
                lat += random.uniform(-1.0, 1.0)
                lng += random.uniform(-1.0, 1.0)

            results.append({
                "district": district_name,
                "ipc_crimes": ipc_count,
                "sll_crimes": sll_count,
                "total_crimes": total_crimes,
                "lat": lat,
                "lng": lng
            })
            
        return results
    except Exception as e:
        print(f"Error parsing district data: {e}")
        return []

if __name__ == "__main__":
    # Test parser
    data = get_district_map_data()
    for d in data[:5]:
        print(d)
