# GOTHAM (Geospatial Operations & Threat/Hotspot Analytics Machine)

Build the Datathon 2026 hackathon project: an advanced intelligence platform for Karnataka State Police with a FastAPI backend, React/Vite frontend, and PostGIS database. This is a deep intelligence engine, moving beyond a basic dashboard to provide probabilistic inference, network analytics, and behavioral profiling.

## User Review Required

> [!IMPORTANT]
> **PostgreSQL & PostGIS**: The backend requires PostgreSQL with PostGIS extensions and the `pg_trgm` extension for trigram similarity (Entity Resolution). We will use a `docker-compose.yml` to spin this up. Ensure Docker is running.

> [!WARNING]
> **OSINT & External APIs**: The OSINT module relies on the Overpass API (OpenStreetMap) and RSS feeds. These are free and require no keys, but require internet access during ingestion/enrichment.

## Open Questions

- We will generate 500 FIRs and seed the required complex patterns (Gang Alpha, Gang Beta, Rajan, Janardhan K). Are there any specific coordinates you want used for the Coastal belt or Bengaluru clusters, or should we randomly select valid coordinates within those regions?
- Do you have Docker Desktop installed to run the PostgreSQL + PostGIS container?

## Proposed Changes

We will create two main directories: `gotham-backend` and `gotham-frontend`, along with a `docker-compose.yml` for the database.

---

### Infrastructure & Database Setup

#### [NEW] docker-compose.yml
- PostgreSQL 15 + PostGIS image (`postgis/postgis:15-3.4`).

---

### Backend (gotham-backend)

The FastAPI backend will serve REST APIs, connect to PostGIS, perform advanced analytics (NetworkX, scikit-learn, fuzzy matching), and handle data ingestion.

#### [NEW] requirements.txt
- `fastapi`, `uvicorn`, `psycopg2-binary`, `sqlalchemy`, `geoalchemy2`, `networkx`, `scikit-learn`, `pandas`, `numpy`, `python-dotenv`, `python-levenshtein`, `metaphone`, `python-louvain`, `feedparser`.

#### [NEW] database.py
- SQLAlchemy setup with PostGIS and pg_trgm extensions.
- Schema definitions including new tables: `VehicleRecord`, `PhysicalDescriptor`, `LocationEntity`, `CrimeSequence`, `GraphMetrics`, `InferredLink`, `OSINTRecord`.

#### [NEW] ingestion/generate_data.py & load_data.py
- Script to generate 500 synthetic FIRs and deep seed specific complex cases:
  - **Gang Alpha**: 8 members, Coastal belt, Dacoity, specific broker/organizer topology.
  - **Gang Beta**: 5 members, Bengaluru, Cybercrime, working hours pattern.
  - **Rajan**: Escalating repeat offender pattern.
  - **Janardhan K**: Entity resolution test case.
- Load script persists all data and relationships into PostGIS.

#### [NEW] graph_engine/*.py
- `builder.py`: Builds NetworkX MultiDiGraph from DB.
- `algorithms.py`: PageRank (influence), Betweenness (brokers), Louvain (communities), Link Prediction (Jaccard + Adamic-Adar).
- `temporal.py`: Time-aware graph snapshots for evolution tracking.
- `inference.py`: Probabilistic link inference and logging.

#### [NEW] intelligence/*.py
- `entity_resolution.py`: Candidate generation (pg_trgm, cosine, fuzzy) and Dempster-Shafer evidence fusion.
- `behavioral.py`: Sequence extraction, escalation detection, Markov chain prediction, rhythm/MO drift analysis.
- `profiling.py`: Dynamic risk scoring and MO profiling.
- `osint.py`: OSM Overpass API and eCourts/News RSS enrichment.

#### [NEW] analytics/*.py
- `clustering.py`: DBSCAN hotspot detection.
- `anomaly.py`: Z-score, Isolation Forest, Graph Anomaly, and Spatio-temporal Co-occurrence fusion.
- `alerts.py`: Multi-signal alert aggregation.
- `similarity.py`: Semantic + structural case similarity.
- `prediction.py`: Random Forest for spatial forecast, Gradient Boosting for reoffense prediction, emergent zone tracking.

#### [NEW] routers/*.py & main.py
- `hotspots.py`, `network.py`, `alerts.py`, `cases.py`, `offenders.py`.
- `intelligence.py`: Inference endpoints (e.g., `/api/intelligence/resolve`).
- `osint.py`: External enrichment endpoints.
- `main.py`: FastAPI application entry point, model loading, graph rebuilding.

---

### Frontend (gotham-frontend)

A React 18 application built with Vite and TailwindCSS, utilizing Cytoscape.js for advanced network visualization.

#### [NEW] package.json
- Dependencies: `react-leaflet`, `leaflet`, `cytoscape`, `recharts`, `axios`, `lucide-react`, `react-router-dom`.

#### [NEW] tailwind.config.js & index.css
- Configured with dark intelligence dashboard theme (navy blue, electric blue accent, danger/warning colors).

#### [NEW] src/components/*
- `Sidebar.jsx`, `TopBar.jsx`, `AlertBanner.jsx`.
- `ConfidenceBar.jsx`: Visualizes inference confidence levels.
- `EvidenceTrail.jsx`: Modal flowchart showing reasoning behind inferences.
- `TemporalSlider.jsx`: Scrubber for navigating graph time snapshots.

#### [NEW] src/pages/*
- `CommandCenter.jsx`: Dashboard with predictive watchlist and multi-signal alerts.
- `HotspotMap.jsx`: Leaflet map with DBSCAN clusters, emergent zones, and OSM data.
- `NetworkGraph.jsx`: Cytoscape.js canvas showing 2-hop criminal network, communities, and inferred links.
- `CaseExplorer.jsx`: FIR list with left/right split panel and similarity scores.
- `OffenderProfile.jsx`: Profile view with behavioral sequence prediction, rhythm, and MO drift.
- `IntelligenceQuery.jsx`: Advanced search for entity resolution with partial inputs.
- `GangAnalysis.jsx`: Visualizes Louvain community detection results and temporal evolution.

#### [NEW] src/App.jsx
- Orchestrates the role switcher and conditionally renders the 7 pages.

## Verification Plan

### Automated / Scripted Verification
- Run `generate_data.py` and `load_data.py` to populate PostGIS and trigger deep seeding.
- Run `build_graph.py` to compute and store initial graph metrics and Louvain communities.
- Start the FastAPI server (`uvicorn main:app`) and verify the deep inference endpoints return 200 OK with explainability metadata.
- Start the Vite development server (`npm run dev`).

### Manual Verification (Extended Demo Flow)
1. **Command Center**: Verify 3 critical alerts and predictive watchlist (Rajan) are visible.
2. **Intelligence Query**: Search for the seeded partial data (scar right hand, blue motorcycle KA-05, chain snatching). Verify Janardhan K is returned with high confidence and evidence trail.
3. **Network Graph**: Expand Janardhan's network, observe community colors and dashed (inferred) links. Verify Ramesh D is highlighted as a primary organizer (PageRank).
4. **Gang Analysis**: Select Community C4, use temporal slider to watch it grow from 2022 to 2023.
5. **Offender Profile (Rajan)**: Verify behavioral sequence predictions (Next predicted: Dacoity) and overdue rhythm flags.
6. **Hotspot Map**: Verify emerging zones layer and hover over a cluster to see OSM enrichment (e.g., nearby ATMs).
