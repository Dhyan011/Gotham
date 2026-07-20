import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, Numeric, Text, Boolean, JSON, ForeignKey, ARRAY
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://gotham:gotham_password@localhost:5432/gotham_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Unit(Base):
    __tablename__ = 'unit'
    unit_id = Column(Integer, primary_key=True, index=True)
    unit_name = Column(String(100))
    district = Column(String(100))
    lat = Column(Numeric(9, 6))
    lng = Column(Numeric(9, 6))

class CaseMaster(Base):
    __tablename__ = 'casemaster'
    fir_id = Column(Integer, primary_key=True, index=True)
    fir_number = Column(String(50))
    unit_id = Column(Integer, ForeignKey('unit.unit_id'))
    crime_type = Column(String(100))
    crime_subtype = Column(String(100))
    date_of_occurrence = Column(DateTime)
    date_reported = Column(DateTime)
    lat = Column(Numeric(9, 6))
    lng = Column(Numeric(9, 6))
    brief_facts = Column(Text)
    status = Column(String(50))
    severity_weight = Column(Integer)
    mo_tags = Column(ARRAY(Text))
    summary = Column(Text)

class Accused(Base):
    __tablename__ = 'accused'
    accused_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    dob = Column(Date)
    gender = Column(String(20))
    address = Column(Text)
    district = Column(String(100))
    risk_score = Column(Numeric(4, 2))
    risk_label = Column(String(20))
    prior_offense_count = Column(Integer)
    mo_pattern = Column(ARRAY(Text))

class CaseAccused(Base):
    __tablename__ = 'caseaccused'
    fir_id = Column(Integer, ForeignKey('casemaster.fir_id'), primary_key=True)
    accused_id = Column(Integer, ForeignKey('accused.accused_id'), primary_key=True)
    role = Column(String(50))

class Victim(Base):
    __tablename__ = 'victim'
    victim_id = Column(Integer, primary_key=True, index=True)
    fir_id = Column(Integer, ForeignKey('casemaster.fir_id'))
    name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(20))
    address = Column(Text)
    occupation = Column(String(100))

class ArrestSurrender(Base):
    __tablename__ = 'arrestsurrender'
    arrest_id = Column(Integer, primary_key=True, index=True)
    accused_id = Column(Integer, ForeignKey('accused.accused_id'))
    fir_id = Column(Integer, ForeignKey('casemaster.fir_id'))
    arrest_date = Column(DateTime)
    arrest_type = Column(String(50))

class VehicleRecord(Base):
    __tablename__ = 'vehiclerecord'
    vehicle_id = Column(Integer, primary_key=True, index=True)
    registration_partial = Column(String(20))
    vehicle_type = Column(String(50))
    color = Column(String(30))
    make = Column(String(50))
    fir_id = Column(Integer, ForeignKey('casemaster.fir_id'))
    confidence = Column(Numeric(3, 2))

class PhysicalDescriptor(Base):
    __tablename__ = 'physicaldescriptor'
    descriptor_id = Column(Integer, primary_key=True, index=True)
    accused_id = Column(Integer, ForeignKey('accused.accused_id'))
    height_cm = Column(Integer)
    build = Column(String(30))
    distinguishing_marks = Column(ARRAY(Text))
    approximate_age_at_filing = Column(Integer)
    source_fir_id = Column(Integer, ForeignKey('casemaster.fir_id'))

class LocationEntity(Base):
    __tablename__ = 'locationentity'
    location_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    location_type = Column(String(50))
    lat = Column(Numeric(9, 6))
    lng = Column(Numeric(9, 6))
    osm_id = Column(Integer)
    crime_affinity = Column(JSON)

class CrimeSequence(Base):
    __tablename__ = 'crimesequence'
    sequence_id = Column(Integer, primary_key=True, index=True)
    accused_id = Column(Integer, ForeignKey('accused.accused_id'))
    ordered_crime_types = Column(ARRAY(Text))
    time_gaps_days = Column(ARRAY(Integer))
    escalation_score = Column(Numeric(4, 2))
    next_predicted_crime = Column(String(100))
    prediction_confidence = Column(Numeric(3, 2))

class GraphMetrics(Base):
    __tablename__ = 'graphmetrics'
    metric_id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(20))
    entity_id = Column(Integer)
    pagerank_score = Column(Numeric(8, 6))
    betweenness_centrality = Column(Numeric(8, 6))
    community_id = Column(Integer)
    computed_at = Column(DateTime)

class InferredLink(Base):
    __tablename__ = 'inferredlink'
    link_id = Column(Integer, primary_key=True, index=True)
    entity_a_type = Column(String(20))
    entity_a_id = Column(Integer)
    entity_b_type = Column(String(20))
    entity_b_id = Column(Integer)
    inference_reason = Column(ARRAY(Text))
    confidence = Column(Numeric(3, 2))
    confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime)

class OSINTRecord(Base):
    __tablename__ = 'osintrecord'
    osint_id = Column(Integer, primary_key=True, index=True)
    fir_id = Column(Integer, ForeignKey('casemaster.fir_id'))
    source = Column(String(100))
    raw_data = Column(JSON)
    extracted_entities = Column(JSON)
    relevance_score = Column(Numeric(3, 2))
    fetched_at = Column(DateTime)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")
