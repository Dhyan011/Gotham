from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="GOTHAM Intelligence API",
    description="Backend for Geospatial Operations & Threat/Hotspot Analytics Machine",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "GOTHAM Deep Intelligence Engine is online."}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "components": ["fastapi"]}

# Routers will be included here as they are built
# app.include_router(hotspots.router, prefix="/api/hotspots", tags=["hotspots"])
