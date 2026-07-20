# GOTHAM - Geospatial Operations & Threat/Hotspot Analytics Machine

> **Datathon 2026** | Crime Intelligence & Analytics Platform for Karnataka State Police (KSP) / SCRB

A deep intelligence engine that transforms raw FIR data into actionable crime intelligence — using graph analytics, behavioral profiling, anomaly detection, and entity resolution.

## Quick Start

### 1. Start the Database
```bash
docker-compose up -d
```

### 2. Backend Setup
```bash
cd gotham-backend
pip install -r requirements.txt

# Generate synthetic data
python -m ingestion.generate_data

# Load into PostgreSQL
python -m ingestion.load_data

# Start the API server
python main.py
```

### 3. Frontend Setup
```bash
cd gotham-frontend
npm install
npm run dev
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI, SQLAlchemy |
| Database | PostgreSQL 15 + PostGIS |
| Graph | NetworkX (PageRank, Louvain, Link Prediction) |
| ML | scikit-learn (DBSCAN, Isolation Forest, Random Forest) |
| Frontend | React 18, Vite, TailwindCSS |
| Maps | Leaflet.js + CartoDB Dark Matter |
| Network Viz | Cytoscape.js |
| Charts | Recharts |

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/dashboard/summary` | Command Center stats |
| `GET /api/hotspots` | DBSCAN crime clusters (GeoJSON) |
| `GET /api/network/{accused_id}` | 2-hop criminal network graph |
| `GET /api/alerts` | Z-score anomaly alerts |
| `GET /api/cases` | Paginated FIR list |
| `GET /api/similar-cases/{fir_id}` | TF-IDF similar cases |
| `GET /api/offenders/{accused_id}` | Full offender intelligence profile |
| `POST /api/intelligence/resolve` | Entity resolution from partial data |
| `GET /api/intelligence/behavioral/{accused_id}` | Behavioral sequence analysis |

## Data

All data is **synthetic** and clearly labeled as simulated. Structurally mirrors real KSP schema with 500 FIRs across 30 Karnataka districts.

---
*GOTHAM Synthetic Dataset v1.0 — Simulated for demonstration purposes*
