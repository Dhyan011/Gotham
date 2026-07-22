"""
GOTHAM Synthetic Data Generator
Generates realistic crime records for Karnataka State Police demo.
Includes deliberate clusters, repeat offenders, and entity resolution targets.
"""
import json
import random
import os
from datetime import datetime, timedelta

random.seed(42)  # Reproducible data for demos

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ─── Karnataka Districts & Police Stations ───────────────────────────────────

KARNATAKA_UNITS = [
    {"unit_id": 1, "unit_name": "Cubbon Park PS", "district": "Bengaluru Urban", "lat": 12.9716, "lng": 77.5946},
    {"unit_id": 2, "unit_name": "Koramangala PS", "district": "Bengaluru Urban", "lat": 12.9352, "lng": 77.6245},
    {"unit_id": 3, "unit_name": "Whitefield PS", "district": "Bengaluru Urban", "lat": 12.9698, "lng": 77.7500},
    {"unit_id": 4, "unit_name": "Jayanagar PS", "district": "Bengaluru Urban", "lat": 12.9250, "lng": 77.5938},
    {"unit_id": 5, "unit_name": "Indiranagar PS", "district": "Bengaluru Urban", "lat": 12.9784, "lng": 77.6408},
    {"unit_id": 6, "unit_name": "Hebbal PS", "district": "Bengaluru North", "lat": 13.0358, "lng": 77.5970},
    {"unit_id": 7, "unit_name": "Yelahanka PS", "district": "Bengaluru North", "lat": 13.1007, "lng": 77.5963},
    {"unit_id": 8, "unit_name": "Devanahalli PS", "district": "Bengaluru Rural", "lat": 13.2473, "lng": 77.7110},
    {"unit_id": 9, "unit_name": "Mysuru North PS", "district": "Mysuru", "lat": 12.3100, "lng": 76.6550},
    {"unit_id": 10, "unit_name": "Mysuru South PS", "district": "Mysuru", "lat": 12.2958, "lng": 76.6394},
    {"unit_id": 11, "unit_name": "Nazarbad PS", "district": "Mysuru", "lat": 12.3150, "lng": 76.6400},
    {"unit_id": 12, "unit_name": "Mangaluru North PS", "district": "Dakshina Kannada", "lat": 12.8714, "lng": 74.8430},
    {"unit_id": 13, "unit_name": "Mangaluru South PS", "district": "Dakshina Kannada", "lat": 12.8500, "lng": 74.8350},
    {"unit_id": 14, "unit_name": "Surathkal PS", "district": "Dakshina Kannada", "lat": 12.9854, "lng": 74.8100},
    {"unit_id": 15, "unit_name": "Udupi Town PS", "district": "Udupi", "lat": 13.3409, "lng": 74.7421},
    {"unit_id": 16, "unit_name": "Kundapur PS", "district": "Udupi", "lat": 13.6263, "lng": 74.6910},
    {"unit_id": 17, "unit_name": "Hubli PS", "district": "Dharwad", "lat": 15.3647, "lng": 75.1240},
    {"unit_id": 18, "unit_name": "Dharwad PS", "district": "Dharwad", "lat": 15.4589, "lng": 75.0078},
    {"unit_id": 19, "unit_name": "Belagavi City PS", "district": "Belagavi", "lat": 15.8497, "lng": 74.4977},
    {"unit_id": 20, "unit_name": "Kalaburagi PS", "district": "Kalaburagi", "lat": 17.3297, "lng": 76.8343},
    {"unit_id": 21, "unit_name": "Raichur PS", "district": "Raichur", "lat": 16.2076, "lng": 77.3463},
    {"unit_id": 22, "unit_name": "Ballari PS", "district": "Ballari", "lat": 15.1394, "lng": 76.9214},
    {"unit_id": 23, "unit_name": "Shivamogga PS", "district": "Shivamogga", "lat": 13.9299, "lng": 75.5681},
    {"unit_id": 24, "unit_name": "Davanagere PS", "district": "Davanagere", "lat": 14.4644, "lng": 75.9218},
    {"unit_id": 25, "unit_name": "Hassan PS", "district": "Hassan", "lat": 13.0072, "lng": 76.0962},
    {"unit_id": 26, "unit_name": "Tumakuru PS", "district": "Tumakuru", "lat": 13.3379, "lng": 77.1173},
    {"unit_id": 27, "unit_name": "Chikkamagaluru PS", "district": "Chikkamagaluru", "lat": 13.3161, "lng": 75.7720},
    {"unit_id": 28, "unit_name": "Mandya PS", "district": "Mandya", "lat": 12.5246, "lng": 76.8953},
    {"unit_id": 29, "unit_name": "Kodagu PS", "district": "Kodagu", "lat": 12.4244, "lng": 75.7382},
    {"unit_id": 30, "unit_name": "Vijayapura PS", "district": "Vijayapura", "lat": 16.8302, "lng": 75.7100},
]

CRIME_TYPE_WEIGHTS = {
    "Theft": 0.30, "Assault": 0.20, "Cybercrime": 0.15,
    "Dacoity": 0.10, "Murder": 0.08, "Fraud": 0.10, "Other": 0.07
}
CRIME_TYPES = list(CRIME_TYPE_WEIGHTS.keys())
CRIME_PROBS = list(CRIME_TYPE_WEIGHTS.values())

STATUSES = ["Under Investigation", "Chargesheet Filed", "Closed", "Referred"]
GENDERS = ["Male", "Female"]
OCCUPATIONS = ["Farmer", "Shopkeeper", "Student", "IT Professional", "Homemaker",
               "Autorickshaw Driver", "Labourer", "Teacher", "Business Owner", "Unemployed"]

SEVERITY_MAP = {"Theft": 3, "Assault": 5, "Cybercrime": 4, "Dacoity": 7, "Murder": 9, "Fraud": 4, "Other": 2}

FIRST_NAMES_MALE = ["Rajan", "Suresh", "Ramesh", "Venkatesh", "Mahesh", "Ganesh", "Arun", "Vijay",
                    "Kumar", "Siddharth", "Naveen", "Prakash", "Rajesh", "Manoj", "Anand",
                    "Deepak", "Srinivas", "Harsha", "Kiran", "Satish", "Janardhan", "Shiva",
                    "Basavaraj", "Manjunath", "Yogesh", "Ashok", "Chandrashekar", "Nagaraj"]
FIRST_NAMES_FEMALE = ["Lakshmi", "Kavitha", "Suma", "Asha", "Priya", "Rekha", "Swathi",
                      "Deepa", "Nandini", "Geetha", "Savitha", "Meera", "Padma"]
LAST_NAMES = ["K", "S", "N", "M", "R", "D", "B", "G", "H", "P", "Reddy", "Gowda", "Shetty",
              "Naik", "Patil", "Hegde", "Rao", "Sharma", "Kumar", "Singh"]

MO_TAGS_POOL = {
    "Theft": ["night break-in", "two-wheeler theft", "mobile snatching", "chain snatching",
              "shoplifting", "house burglary", "vehicle theft", "evening hours"],
    "Assault": ["blunt weapon", "personal enmity", "alcohol-related", "road rage",
                "group attack", "domestic violence", "knife attack"],
    "Cybercrime": ["phishing", "OTP fraud", "social media impersonation", "UPI fraud",
                   "ransomware", "identity theft", "loan app harassment"],
    "Dacoity": ["highway robbery", "armed gang", "home invasion", "vehicle used",
                "coordinated attack", "night operation", "masked assailants"],
    "Murder": ["premeditated", "crime of passion", "property dispute", "honour killing",
               "gang rivalry", "contract killing"],
    "Fraud": ["fake documents", "real estate fraud", "insurance fraud", "cheque bounce",
              "ponzi scheme", "employment fraud"],
    "Other": ["trespassing", "public nuisance", "missing person", "drug possession"]
}

BRIEF_FACTS_TEMPLATES = {
    "Theft": [
        "The complainant reported that unknown persons broke into their residence at {loc} during night hours and stole gold ornaments worth Rs. {val} lakhs. No witnesses were found at the scene.",
        "A two-wheeler (registration {plate}) was stolen from the parking area near {loc}. CCTV footage shows a male suspect in dark clothing fleeing the scene around {time}.",
        "The victim was walking near {loc} when two individuals on a motorcycle snatched their gold chain valued at Rs. {val} lakhs and fled towards the main road.",
        "A mobile phone snatching incident occurred near {loc} bus stop. The suspect grabbed the phone from the victim's hand while riding a two-wheeler.",
    ],
    "Assault": [
        "The accused attacked the victim with a blunt weapon near {loc} following a heated argument over a personal dispute. The victim sustained injuries and was admitted to the district hospital.",
        "A group of {n} individuals assaulted the complainant near {loc} after a road rage incident. The accused used iron rods and stones during the attack.",
        "The accused, in an inebriated state, attacked the victim at {loc} using a knife, causing grievous injuries. The incident appears related to a prior personal enmity.",
    ],
    "Cybercrime": [
        "The complainant received a fraudulent call claiming to be from {bank} bank and was tricked into sharing OTP details, resulting in unauthorized transfer of Rs. {val} lakhs from their account.",
        "Unknown persons created a fake social media profile impersonating the victim and used it to solicit money from their contacts. The fraud was discovered when contacts reported the requests.",
        "The victim received a phishing link via SMS claiming a KYC update was required. Upon clicking, their UPI credentials were compromised and Rs. {val} was debited.",
    ],
    "Dacoity": [
        "A gang of {n} armed individuals intercepted a goods vehicle on {loc} highway, assaulted the driver, and looted cash and valuables worth Rs. {val} lakhs.",
        "The accused, armed with machetes and country-made pistols, broke into the residence at {loc} and robbed the family of gold, cash, and electronics valued at Rs. {val} lakhs.",
        "A coordinated robbery was carried out at {loc} where {n} masked individuals overpowered the security guard and looted the premises.",
    ],
    "Murder": [
        "The victim was found dead with multiple stab wounds near {loc}. Preliminary investigation reveals a property dispute with the accused as the probable motive.",
        "The accused allegedly strangled the victim following a domestic dispute at their residence in {loc}. Neighbors reported hearing loud arguments prior to the incident.",
    ],
    "Fraud": [
        "The accused sold a non-existent plot of land in {loc} to the complainant using forged documents. The fraud was discovered when the victim attempted to register the property.",
        "The complainant was cheated of Rs. {val} lakhs through a fake employment scheme promising government jobs. Multiple victims have come forward with similar complaints.",
    ],
    "Other": [
        "A complaint was filed regarding unauthorized trespassing and public nuisance at {loc}. The accused has been warned previously for similar behavior.",
        "A missing person report was filed for the individual last seen near {loc}. Search operations are underway.",
    ],
}

# ─── Helper Functions ─────────────────────────────────────────────────────────

def random_date(start_year=2022, end_year=2024):
    """Generate a random datetime within the date range."""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days),
                             hours=random.randint(0, 23),
                             minutes=random.randint(0, 59))

def recent_date(days_back=30):
    """Generate a date within the last N days (for spike injection)."""
    now = datetime(2024, 12, 15)  # Fixed 'now' for reproducibility
    return now - timedelta(days=random.randint(0, days_back),
                           hours=random.randint(0, 23))

def jitter(lat, lng, spread=0.05):
    """Add small random noise to coordinates for cluster realism."""
    return round(lat + random.uniform(-spread, spread), 6), \
           round(lng + random.uniform(-spread, spread), 6)

def gen_name(gender="Male"):
    first = random.choice(FIRST_NAMES_MALE if gender == "Male" else FIRST_NAMES_FEMALE)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}"

def gen_brief_facts(crime_type, district):
    template = random.choice(BRIEF_FACTS_TEMPLATES.get(crime_type, BRIEF_FACTS_TEMPLATES["Other"]))
    locations = [f"{district} Main Road", f"{district} Market Area", f"{district} Bus Stand",
                 f"NH-75 near {district}", f"{district} Railway Station area"]
    banks = ["SBI", "HDFC", "ICICI", "Canara", "Axis"]
    return template.format(
        loc=random.choice(locations), val=random.randint(1, 50),
        plate=f"KA-{random.randint(1,55):02d}-{random.choice('ABCDEFGHJKLMNPRSTUVWXY')}-{random.randint(1000,9999)}",
        time=f"{random.randint(18,23)}:{random.choice(['00','15','30','45'])} hrs",
        n=random.randint(3, 8), bank=random.choice(banks)
    )

# ─── Main Data Generators ────────────────────────────────────────────────────

def generate_units():
    with open(os.path.join(DATA_DIR, "units.json"), "w") as f:
        json.dump(KARNATAKA_UNITS, f, indent=2)
    return KARNATAKA_UNITS

def generate_accused():
    """Generate 200 accused with seeded repeat offenders and gangs."""
    accused_list = []

    # ── Gang Alpha: Coastal belt dacoity gang (accused 1-8) ──
    gang_alpha_names = ["Ramesh D", "Suresh N", "Vinay Shetty", "Ashok Naik",
                        "Deepak Hegde", "Manjunath B", "Naveen K", "Siddharth G"]
    for i, name in enumerate(gang_alpha_names, start=1):
        accused_list.append({
            "accused_id": i, "name": name, "dob": f"{random.randint(1985,1998)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "gender": "Male", "address": f"Coastal belt, Karnataka",
            "district": random.choice(["Dakshina Kannada", "Udupi"]),
            "risk_score": round(random.uniform(60, 95), 2),
            "risk_label": "HIGH" if i <= 3 else "MEDIUM",
            "prior_offense_count": random.randint(3, 8),
            "mo_pattern": ["highway robbery", "armed gang", "night operation", "coordinated attack"]
        })

    # ── Gang Beta: Cybercrime network (accused 9-13) ──
    gang_beta_names = ["Kiran Raj", "Srinivas M", "Harsha P", "Yogesh Kumar", "Satish R"]
    for i, name in enumerate(gang_beta_names, start=9):
        accused_list.append({
            "accused_id": i, "name": name, "dob": f"{random.randint(1990,2000)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "gender": "Male",
            "address": "Bengaluru Urban" if i != 13 else "Dharwad",
            "district": "Bengaluru Urban" if i != 13 else "Dharwad",
            "risk_score": round(random.uniform(40, 75), 2),
            "risk_label": "MEDIUM",
            "prior_offense_count": random.randint(2, 5),
            "mo_pattern": ["phishing", "OTP fraud", "social media impersonation", "UPI fraud"]
        })

    # ── Repeat Offender "Rajan" (accused 14) — 7 escalating cases ──
    accused_list.append({
        "accused_id": 14, "name": "Rajan K", "dob": "1988-03-15",
        "gender": "Male", "address": "Jayanagar, Bengaluru",
        "district": "Bengaluru Urban",
        "risk_score": 87.0, "risk_label": "CRITICAL",
        "prior_offense_count": 7,
        "mo_pattern": ["chain snatching", "two-wheeler", "evening hours", "mobile snatching"]
    })

    # ── Entity Resolution Target: Janardhan K (accused 77) ──
    # This is the accused that the "unknown suspect" evidence should match to
    accused_list.append({
        "accused_id": 77, "name": "Janardhan K", "dob": "1991-07-22",
        "gender": "Male", "address": "Jayanagar 4th Block, Bengaluru",
        "district": "Bengaluru Urban",
        "risk_score": 72.0, "risk_label": "HIGH",
        "prior_offense_count": 4,
        "mo_pattern": ["chain snatching", "two-wheeler", "evening hours"]
    })

    # ── Fill remaining accused (15-76, 78-200) ──
    used_ids = {a["accused_id"] for a in accused_list}
    for i in range(15, 201):
        if i in used_ids:
            continue
        gender = random.choice(GENDERS)
        offense_count = random.randint(0, 4)
        crime = random.choices(CRIME_TYPES, CRIME_PROBS)[0]
        risk = round(offense_count * 12 + random.uniform(5, 25), 2)
        accused_list.append({
            "accused_id": i, "name": gen_name(gender),
            "dob": f"{random.randint(1975,2002)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "gender": gender,
            "address": f"{random.choice(KARNATAKA_UNITS)['district']}, Karnataka",
            "district": random.choice(KARNATAKA_UNITS)["district"],
            "risk_score": min(risk, 99.0),
            "risk_label": "HIGH" if risk > 60 else ("MEDIUM" if risk > 30 else "LOW"),
            "prior_offense_count": offense_count,
            "mo_pattern": random.sample(MO_TAGS_POOL.get(crime, ["general"]), min(2, len(MO_TAGS_POOL.get(crime, ["general"]))))
        })

    accused_list.sort(key=lambda x: x["accused_id"])
    with open(os.path.join(DATA_DIR, "accused.json"), "w") as f:
        json.dump(accused_list, f, indent=2)
    return accused_list

def generate_firs(units):
    """
    Generate 500 FIRs with:
    - 3 deliberate crime clusters (Bengaluru cybercrime, Mysuru assault, Coastal dacoity)
    - Chain snatching spike in last 30 days (Bengaluru North)
    - Realistic date spread Jan 2022 – Dec 2024
    """
    firs = []
    fir_counter = 1
    blr_units = [u for u in units if "Bengaluru" in u["district"]]
    mys_units = [u for u in units if u["district"] == "Mysuru"]
    coastal_units = [u for u in units if u["district"] in ("Dakshina Kannada", "Udupi")]

    # ── Cluster 1: Bengaluru cybercrime + theft (80 FIRs) ──
    for _ in range(80):
        unit = random.choice(blr_units)
        crime = random.choice(["Cybercrime", "Theft", "Cybercrime", "Fraud"])
        lat, lng = jitter(unit["lat"], unit["lng"], 0.03)
        dt = random_date()
        firs.append(_make_fir(fir_counter, unit, crime, lat, lng, dt))
        fir_counter += 1

    # ── Cluster 2: Mysuru assault cluster (50 FIRs) ──
    for _ in range(50):
        unit = random.choice(mys_units)
        lat, lng = jitter(12.308, 76.652, 0.02)
        dt = random_date()
        firs.append(_make_fir(fir_counter, unit, "Assault", lat, lng, dt))
        fir_counter += 1

    # ── Cluster 3: Coastal belt dacoity (40 FIRs) ──
    for _ in range(40):
        unit = random.choice(coastal_units) if coastal_units else random.choice(units)
        lat, lng = jitter(unit["lat"], unit["lng"], 0.04)
        dt = random_date()
        firs.append(_make_fir(fir_counter, unit, "Dacoity", lat, lng, dt))
        fir_counter += 1

    # ── Chain snatching spike: Bengaluru North, last 30 days (25 FIRs) ──
    hebbal = next(u for u in units if u["unit_name"] == "Hebbal PS")
    for _ in range(25):
        lat, lng = jitter(hebbal["lat"], hebbal["lng"], 0.02)
        dt = recent_date(30)
        fir = _make_fir(fir_counter, hebbal, "Theft", lat, lng, dt)
        fir["crime_subtype"] = "Chain Snatching"
        fir["mo_tags"] = ["chain snatching", "two-wheeler", "evening hours"]
        fir_counter += 1
        firs.append(fir)

    # ── Rajan's 7 escalating cases ──
    rajan_crimes = [
        ("Theft", datetime(2022, 3, 10, 18, 30)),
        ("Theft", datetime(2022, 7, 22, 19, 0)),
        ("Assault", datetime(2022, 12, 5, 20, 15)),
        ("Assault", datetime(2023, 4, 18, 21, 0)),
        ("Dacoity", datetime(2023, 10, 2, 22, 30)),
        ("Dacoity", datetime(2024, 3, 14, 19, 45)),
        ("Dacoity", datetime(2024, 8, 25, 20, 0)),
    ]
    rajan_fir_ids = []
    for crime, dt in rajan_crimes:
        unit = random.choice(blr_units)
        lat, lng = jitter(unit["lat"], unit["lng"], 0.02)
        fir = _make_fir(fir_counter, unit, crime, lat, lng, dt)
        fir["brief_facts"] = gen_brief_facts(crime, "Bengaluru Urban")
        rajan_fir_ids.append(fir_counter)
        firs.append(fir)
        fir_counter += 1

    # ── Janardhan K's cases (for entity resolution match) ──
    janardhan_fir_ids = []
    for crime, dt in [("Theft", datetime(2023, 6, 15, 19, 0)), ("Theft", datetime(2024, 1, 20, 18, 30)),
                      ("Theft", datetime(2024, 7, 10, 19, 45)), ("Assault", datetime(2024, 10, 5, 20, 0))]:
        unit = random.choice(blr_units)
        lat, lng = jitter(12.925, 77.594, 0.015)  # Near Jayanagar
        fir = _make_fir(fir_counter, unit, crime, lat, lng, dt)
        fir["mo_tags"] = ["chain snatching", "two-wheeler", "evening hours"]
        janardhan_fir_ids.append(fir_counter)
        firs.append(fir)
        fir_counter += 1

    # ── Fill remaining generic FIRs ──
    remaining = 500 - len(firs)
    for _ in range(remaining):
        unit = random.choice(units)
        crime = random.choices(CRIME_TYPES, CRIME_PROBS)[0]
        lat, lng = jitter(unit["lat"], unit["lng"], 0.08)
        dt = random_date()
        firs.append(_make_fir(fir_counter, unit, crime, lat, lng, dt))
        fir_counter += 1

    firs = firs[:500]  # Ensure exactly 500
    with open(os.path.join(DATA_DIR, "firs.json"), "w") as f:
        json.dump(firs, f, indent=2, default=str)

    # Save special FIR ID mappings for linking
    with open(os.path.join(DATA_DIR, "seeded_ids.json"), "w") as f:
        json.dump({"rajan_fir_ids": rajan_fir_ids, "janardhan_fir_ids": janardhan_fir_ids}, f, indent=2)

    return firs

def _make_fir(fir_id, unit, crime_type, lat, lng, dt):
    severity = SEVERITY_MAP.get(crime_type, 3) + random.randint(-1, 2)
    return {
        "fir_id": fir_id,
        "fir_number": f"FIR/{dt.year}/{unit['district'][:3].upper()}/{fir_id:04d}",
        "unit_id": unit["unit_id"],
        "crime_type": crime_type,
        "crime_subtype": "General",
        "date_of_occurrence": dt.isoformat(),
        "date_reported": (dt + timedelta(hours=random.randint(1, 48))).isoformat(),
        "lat": lat, "lng": lng,
        "brief_facts": gen_brief_facts(crime_type, unit["district"]),
        "status": random.choice(STATUSES),
        "severity_weight": max(1, min(10, severity)),
        "mo_tags": random.sample(MO_TAGS_POOL.get(crime_type, ["general"]),
                                 min(random.randint(1, 3), len(MO_TAGS_POOL.get(crime_type, ["general"])))),
        "summary": f"{crime_type} incident reported at {unit['unit_name']}, {unit['district']}."
    }

def generate_case_accused(firs, accused_list):
    """Link accused to FIRs. Create deliberate gang linkages and repeat offender connections."""
    links = []
    used_pairs = set()
    seeded = json.load(open(os.path.join(DATA_DIR, "seeded_ids.json")))

    # ── Gang Alpha: link accused 1-8 to coastal dacoity FIRs ──
    coastal_firs = [f for f in firs if f["crime_type"] == "Dacoity" and f["fir_id"] <= 170]
    for fir in coastal_firs[:15]:
        members = random.sample(range(1, 9), random.randint(2, 4))
        for acc_id in members:
            pair = (fir["fir_id"], acc_id)
            if pair not in used_pairs:
                links.append({"fir_id": fir["fir_id"], "accused_id": acc_id, "role": "Gang Member"})
                used_pairs.add(pair)

    # ── Gang Beta: link accused 9-13 to cybercrime FIRs ──
    cyber_firs = [f for f in firs if f["crime_type"] in ("Cybercrime", "Fraud") and f["fir_id"] <= 80]
    for fir in cyber_firs[:10]:
        members = random.sample(range(9, 14), random.randint(2, 3))
        for acc_id in members:
            pair = (fir["fir_id"], acc_id)
            if pair not in used_pairs:
                links.append({"fir_id": fir["fir_id"], "accused_id": acc_id, "role": "Accused"})
                used_pairs.add(pair)

    # ── Rajan (accused 14) linked to his 7 FIRs ──
    for fir_id in seeded["rajan_fir_ids"]:
        pair = (fir_id, 14)
        if pair not in used_pairs:
            links.append({"fir_id": fir_id, "accused_id": 14, "role": "Main Accused"})
            used_pairs.add(pair)

    # ── Janardhan K (accused 77) linked to his FIRs ──
    for fir_id in seeded["janardhan_fir_ids"]:
        pair = (fir_id, 77)
        if pair not in used_pairs:
            links.append({"fir_id": fir_id, "accused_id": 77, "role": "Main Accused"})
            used_pairs.add(pair)

    # ── Random linkages for remaining FIRs ──
    remaining_firs = [f for f in firs if not any(l["fir_id"] == f["fir_id"] for l in links)]
    acc_ids = [a["accused_id"] for a in accused_list]
    for fir in remaining_firs:
        num_accused = random.randint(1, 3)
        for acc_id in random.sample(acc_ids, num_accused):
            pair = (fir["fir_id"], acc_id)
            if pair not in used_pairs:
                links.append({"fir_id": fir["fir_id"], "accused_id": acc_id, "role": "Accused"})
                used_pairs.add(pair)

    with open(os.path.join(DATA_DIR, "case_accused.json"), "w") as f:
        json.dump(links, f, indent=2)
    return links

def generate_victims(firs):
    """Generate ~400 victims linked to FIRs."""
    victims = []
    victim_id = 1
    for fir in random.sample(firs, min(350, len(firs))):
        num_victims = random.randint(1, 2) if victim_id < 390 else 1
        for _ in range(num_victims):
            if victim_id > 400:
                break
            gender = random.choice(GENDERS)
            victims.append({
                "victim_id": victim_id,
                "fir_id": fir["fir_id"],
                "name": gen_name(gender),
                "age": random.randint(18, 70),
                "gender": gender,
                "address": f"{random.choice(KARNATAKA_UNITS)['district']}, Karnataka",
                "occupation": random.choice(OCCUPATIONS)
            })
            victim_id += 1
    with open(os.path.join(DATA_DIR, "victims.json"), "w") as f:
        json.dump(victims, f, indent=2)
    return victims

def generate_physical_descriptors():
    """Generate physical descriptors for key accused (entity resolution data)."""
    descriptors = [
        # Janardhan K — 2 records from different FIRs (slightly inconsistent for ER demo)
        {"descriptor_id": 1, "accused_id": 77, "height_cm": 175, "build": "thin",
         "distinguishing_marks": ["scar right hand", "mole on neck"],
         "approximate_age_at_filing": 32, "source_fir_id": None},
        {"descriptor_id": 2, "accused_id": 77, "height_cm": 178, "build": "medium",
         "distinguishing_marks": ["scar right hand"],
         "approximate_age_at_filing": 33, "source_fir_id": None},
        # Rajan
        {"descriptor_id": 3, "accused_id": 14, "height_cm": 170, "build": "medium",
         "distinguishing_marks": ["scar left cheek", "tattoo right arm"],
         "approximate_age_at_filing": 35, "source_fir_id": None},
        {"descriptor_id": 4, "accused_id": 14, "height_cm": 172, "build": "medium",
         "distinguishing_marks": ["scar left cheek"],
         "approximate_age_at_filing": 36, "source_fir_id": None},
    ]
    with open(os.path.join(DATA_DIR, "physical_descriptors.json"), "w") as f:
        json.dump(descriptors, f, indent=2)
    return descriptors

def generate_vehicle_records():
    """Generate vehicle records for entity resolution targets."""
    vehicles = [
        {"vehicle_id": 1, "registration_partial": "KA-05-H-3", "vehicle_type": "Motorcycle",
         "color": "Blue", "make": "Bajaj Pulsar", "fir_id": None, "confidence": 0.75},
        {"vehicle_id": 2, "registration_partial": "KA-05-HB-34", "vehicle_type": "Motorcycle",
         "color": "Blue", "make": "Bajaj Pulsar", "fir_id": None, "confidence": 0.90},
        {"vehicle_id": 3, "registration_partial": "KA-01-MN-", "vehicle_type": "Motorcycle",
         "color": "Red", "make": "Honda Activa", "fir_id": None, "confidence": 0.60},
    ]
    with open(os.path.join(DATA_DIR, "vehicle_records.json"), "w") as f:
        json.dump(vehicles, f, indent=2)
    return vehicles

def generate_arrests(case_accused_links):
    """Generate arrest records for a subset of case-accused links."""
    arrests = []
    arrest_id = 1
    for link in random.sample(case_accused_links, min(150, len(case_accused_links))):
        arrests.append({
            "arrest_id": arrest_id,
            "accused_id": link["accused_id"],
            "fir_id": link["fir_id"],
            "arrest_date": (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 700))).isoformat(),
            "arrest_type": random.choice(["Arrest", "Surrender", "Warrant"])
        })
        arrest_id += 1
    with open(os.path.join(DATA_DIR, "arrests.json"), "w") as f:
        json.dump(arrests, f, indent=2)
    return arrests

# ─── Main Entry Point ─────────────────────────────────────────────────────────

def main():
    print("🔧 GOTHAM Data Generator — Generating synthetic Karnataka crime data...")
    print("─" * 60)

    units = generate_units()
    print(f"✅ Generated {len(units)} police units across Karnataka")

    accused = generate_accused()
    print(f"✅ Generated {len(accused)} accused (incl. Gang Alpha, Gang Beta, Rajan, Janardhan K)")

    firs = generate_firs(units)
    print(f"✅ Generated {len(firs)} FIRs with 3 clusters + chain snatching spike")

    links = generate_case_accused(firs, accused)
    print(f"✅ Generated {len(links)} case-accused links")

    victims = generate_victims(firs)
    print(f"✅ Generated {len(victims)} victims")

    descriptors = generate_physical_descriptors()
    print(f"✅ Generated {len(descriptors)} physical descriptors")

    vehicles = generate_vehicle_records()
    print(f"✅ Generated {len(vehicles)} vehicle records")

    arrests = generate_arrests(links)
    print(f"✅ Generated {len(arrests)} arrest records")

    print("─" * 60)
    print(f"📁 All data saved to: {os.path.abspath(DATA_DIR)}")
    print("🚀 Ready for ingestion with load_data.py")

if __name__ == "__main__":
    main()
