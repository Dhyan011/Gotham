# GOTHAM - Geospatial Operations & Threat/Hotspot Analytics Machine

> [!IMPORTANT]
> This is NOT a basic crime dashboard. GOTHAM is a deep intelligence engine for Karnataka State Police (KSP) / SCRB, built for Datathon 2026.

**The Core Philosophy**: An investigator should be able to feed GOTHAM the smallest fragment of information — a partial name, a vehicle description, a location and time — and get back a ranked, evidence-backed intelligence report connecting that fragment to the full crime graph.

## System Architecture

### Backend (`gotham-backend/`)
```text
gotham-backend/
├── main.py
├── database.py
├── graph_engine/
│   ├── builder.py          # Builds NetworkX multigraph from DB
│   ├── algorithms.py       # PageRank, Betweenness, Louvain, Link Prediction
│   ├── temporal.py         # Time-aware graph snapshots
│   └── inference.py        # Probabilistic link inference
├── intelligence/
│   ├── entity_resolution.py   # Fuzzy match partial descriptors → candidates
│   ├── behavioral.py          # Sequential pattern mining on offender history
│   ├── profiling.py           # Dynamic risk scoring + MO profiling
│   └── osint.py               # External data enrichment layer
├── analytics/
│   ├── clustering.py          # DBSCAN + HDBSCAN hotspot detection
│   ├── anomaly.py             # Isolation Forest + LSTM autoencoder
│   ├── alerts.py              # Multi-signal alert fusion
│   ├── similarity.py          # Semantic + structural case similarity
│   └── prediction.py          # Crime forecast model
├── ingestion/
│   ├── generate_data.py
│   ├── load_data.py
│   ├── build_graph.py
│   └── llm_enrich.py
└── routers/
    ├── hotspots.py
    ├── network.py
    ├── alerts.py
    ├── cases.py
    ├── offenders.py
    ├── intelligence.py      # New: deep inference endpoints
    └── osint.py             # New: external enrichment endpoints
```

### Frontend (`gotham-frontend/`)
```text
gotham-frontend/
├── src/
│   ├── pages/
│   │   ├── CommandCenter.jsx
│   │   ├── HotspotMap.jsx
│   │   ├── NetworkGraph.jsx        # Upgraded: full graph analytics UI
│   │   ├── CaseExplorer.jsx
│   │   ├── OffenderProfile.jsx
│   │   ├── IntelligenceQuery.jsx   # New: minimal input → max inference
│   │   └── GangAnalysis.jsx        # New: community detection results
│   └── components/
│       ├── Sidebar.jsx
│       ├── TopBar.jsx
│       ├── AlertBanner.jsx
│       ├── ConfidenceBar.jsx       # New: shows inference confidence
│       ├── EvidenceTrail.jsx       # New: shows why a connection was made
│       └── TemporalSlider.jsx      # New: scrub through time on graph
```

## Database Schema (Extended)

*(All previous tables remain. Add these:)*

```sql
CREATE TABLE VehicleRecord (
  vehicle_id SERIAL PRIMARY KEY,
  registration_partial VARCHAR(20),  -- may be incomplete
  vehicle_type VARCHAR(50),
  color VARCHAR(30),
  make VARCHAR(50),
  fir_id INT REFERENCES CaseMaster(fir_id),
  confidence DECIMAL(3,2)            -- how certain is this sighting
);

CREATE TABLE PhysicalDescriptor (
  descriptor_id SERIAL PRIMARY KEY,
  accused_id INT REFERENCES Accused(accused_id),
  height_cm INT,
  build VARCHAR(30),
  distinguishing_marks TEXT[],       -- ['scar left cheek', 'tattoo right arm']
  approximate_age_at_filing INT,
  source_fir_id INT REFERENCES CaseMaster(fir_id)
);

CREATE TABLE LocationEntity (
  location_id SERIAL PRIMARY KEY,
  name VARCHAR(200),
  location_type VARCHAR(50),         -- ATM, School, Bar, Market, Highway
  lat DECIMAL(9,6),
  lng DECIMAL(9,6),
  osm_id BIGINT,                     -- OpenStreetMap ID if enriched
  crime_affinity JSONB               -- {crime_type: frequency} computed field
);

CREATE TABLE CrimeSequence (
  sequence_id SERIAL PRIMARY KEY,
  accused_id INT REFERENCES Accused(accused_id),
  ordered_crime_types TEXT[],        -- ['Theft','Assault','Dacoity'] in order
  time_gaps_days INT[],              -- days between each offense
  escalation_score DECIMAL(4,2),    -- computed: is severity increasing?
  next_predicted_crime VARCHAR(100), -- from sequence model
  prediction_confidence DECIMAL(3,2)
);

CREATE TABLE GraphMetrics (
  metric_id SERIAL PRIMARY KEY,
  entity_type VARCHAR(20),           -- Accused / Location / Station
  entity_id INT,
  pagerank_score DECIMAL(8,6),
  betweenness_centrality DECIMAL(8,6),
  community_id INT,                  -- Louvain community assignment
  computed_at TIMESTAMP
);

CREATE TABLE InferredLink (
  link_id SERIAL PRIMARY KEY,
  entity_a_type VARCHAR(20),
  entity_a_id INT,
  entity_b_type VARCHAR(20),
  entity_b_id INT,
  inference_reason TEXT[],           -- ['shared location', 'same MO', 'time overlap']
  confidence DECIMAL(3,2),
  confirmed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP
);

CREATE TABLE OSINTRecord (
  osint_id SERIAL PRIMARY KEY,
  fir_id INT REFERENCES CaseMaster(fir_id),
  source VARCHAR(100),               -- 'eCourts', 'NewsAPI', 'OSM'
  raw_data JSONB,
  extracted_entities JSONB,          -- names, locations, dates found
  relevance_score DECIMAL(3,2),
  fetched_at TIMESTAMP
);
```

## Module 1: Entity Resolution Engine
**File**: `intelligence/entity_resolution.py`

**Problem**: Investigator has partial information about a suspect. Input can be any combination of:
- Partial name (phonetic variants)
- Physical descriptors (height, build, marks)
- Vehicle partial registration or description
- Crime type + location + time window
- Known associates

### Algorithm Pipeline

**Step 1 — Candidate Generation**
For each input signal, independently query DB:
- **Name**: use pg_trgm trigram similarity (threshold 0.3), also try Soundex + Metaphone phonetic matching
- **Physical**: cosine similarity on descriptor vectors
- **Vehicle**: fuzzy regex on partial registration
- **Location+Time**: spatial query within radius + time window
Each signal returns a candidate set with signal-specific scores.

**Step 2 — Evidence Fusion (Dempster-Shafer combination)**
Combine evidence from multiple weak signals into a single belief score per candidate:
`belief(candidate) = 1 - PRODUCT(1 - signal_score_i)` *(normalized across all candidates)*
*This means: one strong signal OR multiple weak signals both raise belief. No single signal is required.*

**Step 3 — Ranking + Explanation**
Return top 10 candidates with:
- Overall confidence score (0-1)
- Evidence breakdown: which signals matched and how strongly
- Contradicting evidence: signals that do NOT match
- Similar past cases linked to this candidate

**Implementation Notes:**
- Install: `pip install python-levenshtein metaphone`
- Use psycopg2 for pg_trgm queries
- Build descriptor feature vectors with sklearn

### API Endpoint
`POST /api/intelligence/resolve`

**Body:**
```json
{
  "partial_name": "Rajan K",
  "physical": {"marks": ["scar left cheek"], "build": "medium"},
  "vehicle": {"type": "motorcycle", "color": "red"},
  "location": {"lat": 12.93, "lng": 77.58},
  "time_window": {"from": "2024-11-01", "to": "2024-11-30"},
  "crime_type": "Chain Snatching"
}
```

**Response:**
```json
{
  "candidates": [
    {
      "accused_id": 47,
      "name": "Rajanna K",
      "confidence": 0.87,
      "evidence": {
        "name_similarity": 0.82,
        "physical_match": 0.91,
        "vehicle_match": 0.75,
        "location_overlap": 0.94,
        "mo_match": 0.88
      },
      "contradictions": ["age: suspect described as 30s, record shows 44"],
      "linked_cases": [12, 47, 103],
      "risk_score": 91
    }
  ]
}
```

## Module 2: Deep Graph Analytics Engine
**File**: `graph_engine/algorithms.py`

Build a NetworkX MultiDiGraph where:
- **Nodes**: Accused, Victim, Location, CaseMaster, Unit
- **Edges**: 
  - accused→case (INVOLVED_IN, weight=severity)
  - accused→accused (CO_ACCUSED, weight=shared_case_count)
  - accused→location (OPERATES_AT, weight=frequency)
  - case→location (OCCURRED_AT)
  - victim→case (VICTIMIZED_IN)
  - location→location (ADJACENT, weight=distance_km)

**Algorithm 1: Weighted PageRank**
- **Purpose**: Find most INFLUENTIAL nodes in criminal network (not most arrested — the organizer who appears less but connects more)
- `nx.pagerank(G, weight='weight', alpha=0.85)`
- **Interpret**: High PageRank accused = network hub = likely organizer. Store results in GraphMetrics table.

**Algorithm 2: Betweenness Centrality**
- **Purpose**: Find BROKERS — accused who connect otherwise separate groups. These are key targets: removing them fragments the network.
- `nx.betweenness_centrality(G, weight='weight', normalized=True)`
- **Visualize**: nodes sized by betweenness score in Cytoscape

**Algorithm 3: Community Detection (Louvain)**
- **Purpose**: Automatically identify GANG CLUSTERS without manual tagging
- **Install**: `pip install python-louvain` (`import community as community_louvain`)
- Convert to undirected for Louvain:
  ```python
  G_undirected = G.to_undirected()
  partition = community_louvain.best_partition(G_undirected)
  ```
- Each community = potential gang or organized crime group. Color-code communities in Cytoscape visualization. Compute community statistics: size, dominant crime type, geographic spread.

**Algorithm 4: Link Prediction**
- **Purpose**: Infer PROBABLE connections not yet in the database. Use Jaccard coefficient + Adamic-Adar index on accused nodes:
  - For each pair of accused NOT directly connected:
    - `jaccard = |common_neighbors| / |union_neighbors|`
    - `adamic_adar = sum(1/log(degree(n)) for n in common_neighbors)`
  - Flag pairs with high scores as InferredLink records.
  - Threshold: `jaccard > 0.3 OR adamic_adar > 1.5`
- These show up in UI as dashed edges: "Probable connection - not confirmed"

**Algorithm 5: Temporal Graph Analysis**
- **File**: `graph_engine/temporal.py`
- Build separate graph snapshots per quarter (2022Q1 ... 2024Q4). Track per accused across snapshots:
  - degree growth rate (accelerating = escalating criminal activity)
  - new community memberships (gang switching / expansion)
  - geographic spread increase (fleeing or expanding)
- **API**: `GET /api/network/temporal/{accused_id}`
- **Returns**: time series of network metrics per quarter
- **Frontend**: `TemporalSlider.jsx` — drag to replay network evolution

## Module 3: Behavioral Sequence Intelligence
**File**: `intelligence/behavioral.py`

For each accused with 3+ prior offenses, compute:

**Step 1 — Crime Sequence Extraction**
- Order all linked FIRs by `date_of_occurrence`
- Extract: `[crime_type_1, crime_type_2, ..., crime_type_n]`
- Extract: `[days_gap_1, days_gap_2, ..., days_gap_n-1]`

**Step 2 — Escalation Detection**
- Assign severity weights: Theft=2, Fraud=3, Assault=4, Dacoity=6, Murder=9, Cybercrime=3
- Compute linear regression slope on severity over time. `escalation_score = slope * recency_weight`
- If slope > 0.5: flagged as ESCALATING offender

**Step 3 — Next Crime Prediction (N-gram Markov chain)**
- Build transition matrix from ALL offender histories in DB: `P(next_crime | last_two_crimes)`
- For each accused: predict most likely next crime type. Store in `CrimeSequence.next_predicted_crime`
- **Example output**: *"Based on sequence [Theft → Assault → Assault], predicted next: Dacoity (confidence: 0.67)"*

**Step 4 — Rhythm Analysis**
- Average time gap between offenses = personal recidivism rhythm
- If `last_offense` was X days ago and `X > avg_gap * 1.5`: → **"Overdue"** flag: may be planning next offense
- If time gaps are decreasing: → **"Accelerating"** flag: increasing frequency

**Step 5 — MO Drift Detection**
- Compare MO tags between first half and second half of history
- Significant change = learning/adapting criminal
- Flag: *"MO drift detected — methods changing since 2023"*

### API Endpoint
`GET /api/intelligence/behavioral/{accused_id}`
**Returns:**
```json
{
  "sequence": [],
  "escalation_score": 0.0,
  "escalation_flag": false,
  "next_predicted_crime": "",
  "prediction_confidence": 0.0,
  "recidivism_rhythm_days": 0,
  "rhythm_flag": "",
  "mo_drift_detected": false,
  "mo_drift_description": ""
}
```

## Module 4: Multi-Signal Anomaly Detection
**File**: `analytics/anomaly.py`

- **Signal 1: Statistical (Z-score)** — already designed
  - `z = (current_30d - rolling_mean_6m) / rolling_std_6m`
  - Flag if `z > 2.0`
- **Signal 2: Isolation Forest (sklearn)**
  - Features per FIR: `[hour_of_day, day_of_week, lat, lng, severity_weight, victim_age, accused_count]`
  - Train `IsolationForest(contamination=0.05)` on historical data
  - Score each new FIR: anomaly_score ∈ [-1, 1]. Flag if score < -0.3 as anomalous incident
- **Signal 3: Graph Anomaly**
  - Monitor accused node degree over rolling 30-day window
  - Flag if degree increase > 2 std deviations above personal baseline. Meaning: accused suddenly appearing in many new cases = active spree
- **Signal 4: Spatio-temporal Co-occurrence**
  - Flag when: unusual crime type + unusual location + unusual time all occur together simultaneously
  - Use 3D kernel density estimation (`scipy.stats.gaussian_kde`) on (lat, lng, hour_of_day) space

**Fusion**: Combine all 4 signals per incident
- `combined_anomaly_score = weighted_average(signal_scores)`
- `weights = [0.25, 0.30, 0.25, 0.20]`
- Alert levels:
  - score > 0.8: **CRITICAL**
  - score > 0.6: **HIGH**
  - score > 0.4: **MEDIUM**

### API Endpoint
`GET /api/alerts/anomalies`
Returns alerts with full signal breakdown:
> "This incident is anomalous because:
> [CRITICAL] Z-score 3.2 in chain snatching for Bengaluru North
> [HIGH] Isolation Forest flags unusual victim profile
> [MEDIUM] Graph: accused degree spiked 4x this week"

## Module 5: OSINT Enrichment Layer
**File**: `intelligence/osint.py`

Connect to these external sources at ingestion + on-demand:

**Source 1: OpenStreetMap (Overpass API)**
- For each crime location, query OSM within 500m radius: ATMs/banks, Schools/colleges, Bars/liquor shops, Bus stands/railway stations, Industrial areas.
- API call (free, no key needed): `https://overpass-api.de/api/interpreter`
- Query: `[out:json]; node(around:500,{lat},{lng})[amenity]; out;`
- Enrich `LocationEntity.crime_affinity` with venue context. UI: hovering a crime cluster shows "Near 3 ATMs, 1 school"

**Source 2: eCourts Public API**
- `https://ecourts.gov.in/ecourts_home/`
- Search by accused name for public court records to match conviction history.

**Source 3: News Correlation (NewsAPI or RSS)**
- For each FIR date + district, search local Kannada/English news (RSS feeds from Deccan Herald, Times of India Karnataka).
- Look for coverage of same incident, named suspects, linked events. Parse with `feedparser`.

**Source 4: Synthetic Social Graph Inference**
- Build inference: Co-location pattern (two accused appearing near same location within 2 hours on 3+ separate occasions → infer association) and Time-correlation (crimes happening in coordinated time windows across districts → infer gang coordination signal).

*All OSINT results are clearly labeled with source and confidence, never presented as confirmed fact, and always shown as "External signal — unverified".*

**API Endpoints:**
- `POST /api/osint/enrich/{fir_id}`
- `GET /api/osint/accused/{accused_id}`

## Module 6: Predictive Crime Forecasting
**File**: `analytics/prediction.py`

**Model 1: Spatial Crime Forecast**
- **Features**: `[district, crime_type, month, day_of_week, local_event_flag, historical_count_same_period]`
- **Model**: Random Forest Regressor (sklearn)
- **Output**: predicted_incident_count per (district, crime_type, week). Display as "Expected incidents next 7 days" overlay on map.

**Model 2: Repeat Offense Prediction**
- **Features per accused**: `[days_since_last_offense, total_offenses, escalation_score, avg_time_gap, community_size, betweenness_rank]`
- **Model**: Gradient Boosting Classifier (sklearn)
- **Output**: P(reoffend within 30 days) per accused. Flag top 10 highest-probability as "Imminent Risk" list on Command Center.

**Model 3: Hotspot Emergence Prediction**
- For each spatial grid cell (0.1° × 0.1°): Compute trend (is crime count increasing over last 4 weeks?). Use linear regression slope as emergence score.
- Map overlay: "Emerging zones" shown as orange gradient (separate from established hotspots).

**API Endpoints:**
- `GET /api/predictions/hotspots?weeks_ahead=2`
- `GET /api/predictions/reoffense`
- `GET /api/predictions/emergence`

## Frontend Pages

### Intelligence Query Page
**File**: `src/pages/IntelligenceQuery.jsx`
An investigator enters ANY fragment of information.

**UI Layout:**
- **Left panel**: Input form with all optional fields (Partial name, Physical description, Vehicle, Location, Date/time range, Crime type, Known associates, Free text)
- **Right panel**: Ranked candidate list with confidence bars (`ConfidenceBar.jsx`). 
- **EvidenceTrail.jsx Modal**: Visual flowchart showing inference chain.
  - *[Input: red Pulsar motorcycle] → matches VehicleRecord #47 (confidence 0.75) → linked to FIR/2024/MYS/0231 → accused_id 103 (Rajanna K) → Rajanna has 3 prior chain snatching cases → 2 of those in same 5km radius as input location. OVERALL CONFIDENCE: 0.87*

### Gang Analysis Page
**File**: `src/pages/GangAnalysis.jsx`
Visualizes Louvain community detection results.

- **Left panel**: Community list showing ID, size, dominant crime type, centroid, highest PageRank member, highest betweenness member, timeline of growth.
- **Right panel**: Full graph colored by community. Node size = betweenness centrality, Node brightness = PageRank score, Dashed edges = InferredLink.
- **Clicking a community**: Shows community intelligence report (e.g., *"Community C4: 12 members, primarily Dacoity, active in Coastal belt since Q3 2023, Probable organizer: Ramesh D, Key broker: Suresh N"*).

## Synthetic Data: Deep Seeding
Beyond basic 500 FIRs, seed these specific patterns:

- **Gang Alpha (Community detection target)**: 8 accused, linked through 15 FIRs, Dacoity + Assault. Active in Coastal belt. Two brokers, one organizer.
- **Gang Beta (Cybercrime network)**: 5 accused, Bengaluru Urban + one in Hubballi (broker). Crime type: Cybercrime + Fraud. Time pattern: only on weekdays, 10am-4pm.
- **Repeat Offender "Rajan"**: 7 cases, escalating severity (Theft → Assault → Dacoity). Predicted next: Dacoity. Has 2 physical descriptor records across different FIRs.
- **Entity Resolution Test Case**: Seed a "John Doe" (unknown suspect). Physical: "tall, thin build, scar right hand, yellow shirt". Vehicle: "blue motorcycle, partial plate KA-05". Should match Accused #77 "Janardhan K" with confidence 0.79.
- **Temporal Evolution Seed**: Gang Alpha starts as 3 members in 2022Q1. Grows to 8 members by 2023Q3. Member #4 joins mid-2022.

## Explainability Requirements
Every single AI/ML output MUST include an explanation layer:

- **Risk Score**: *"Prior offenses: 7 cases (score: 38/40)... TOTAL: 87/100"*
- **Anomaly Alert**: *"Z-score: 3.2... Isolation Forest: anomaly score -0.61... Graph: Rajan's degree increased... Combined signal: 0.84 — CRITICAL"*
- **Predicted Link**: *"Probable connection between Ramesh D and Suresh N: 3 common associates (Jaccard: 0.45)... NOT CONFIRMED"*
- **Community Assignment**: *"Placed in Community C4 because: 8 of 12 direct connections are C4 members..."*

## Coding Standards
- Every module has standalone `__main__` test that can run independently.
- All DB queries use parameterized statements (no string interpolation).
- Graph is rebuilt from DB at startup + can be triggered via `POST /api/admin/rebuild-graph`.
- All ML models serialized with joblib after first training run, loaded from disk on subsequent starts.
- Every API response includes metadata (data_source, algorithm_used, computed_at, confidence_note).
- `inference.py` logs every link inference with full evidence trail to InferredLink table.

## What Makes This Genuinely Hard
1. **Entity resolution under uncertainty** (Dempster-Shafer probabilistic multi-signal fusion)
2. **Link prediction** (Jaccard + Adamic-Adar surface probable unknown connections)
3. **Temporal graph evolution** (animate network growth, detect structural changes)
4. **Behavioral sequence prediction** (Markov chain on crime types)
5. **Community detection** (Louvain automatic gang discovery)
6. **Multi-signal anomaly fusion** (4-signal fusion with weighted confidence)
7. **OSINT enrichment** (External venue context enriches every crime location)
8. **Explainability everywhere** (Output the reasoning chain behind every number)

## Demo Flow (Upgraded)
**90-second to 3-minute extended demo:**
- `[0:00]` **Command Center loads** → 3 critical alerts visible, watchlist shows "Rajan: 0.84 reoffense probability".
- `[0:20]` **Intelligence Query page** → Investigator types: "male, scar right hand, blue motorcycle KA-05, chain snatching near Jayanagar, November 2024" → GOTHAM returns: "Janardhan K — confidence 0.87" → Expand evidence trail shows exactly why.
- `[0:50]` **Click "Investigate" → Network Graph** → Janardhan's 2-hop network loads → Community detection color shows C4 → Probable link to Ramesh D appears → Node sizes show Ramesh D is the PageRank #1 (organizer).
- `[1:20]` **Gang Analysis page** → C4 highlighted → Temporal slider dragged back to 2022 (only 3 members) → Slide forward to watch gang grow.
- `[1:50]` **Offender Profile: Rajan** → Behavioral sequence shown (Predicted next: Dacoity) → Rhythm flag: OVERDUE → MO drift flagged.
- `[2:20]` **Hotspot Map** → Predictive overlay active (2 emerging zones) → Mangaluru cluster pulsing (C4 territory) → OSM enrichment shows nearby ATMs.
