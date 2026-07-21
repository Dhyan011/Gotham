import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from pgvector.sqlalchemy import Vector

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://gotham:gotham_password@localhost:5432/gotham_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =====================================================================
# GOTHAM ONTOLOGY SCHEMA (Hackathon Edition)
# =====================================================================

class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    risk_score = Column(Float, default=0.0) # XGBoost cached output
    
    # Relationships
    firs_involved = relationship("FIR", secondary="person_fir_map", back_populates="people")
    vehicles_owned = relationship("Vehicle", back_populates="owner")

class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

class FIR(Base):
    __tablename__ = "fir"
    id = Column(Integer, primary_key=True, autoincrement=True)
    crime_no = Column(String, unique=True, index=True)
    date_registered = Column(Date)
    crime_type = Column(String)
    description = Column(Text)
    
    # Semantic Search Vector (384 dims for sentence-transformers 'all-MiniLM-L6-v2')
    embedding = Column(Vector(384))
    
    location_id = Column(Integer, ForeignKey("location.id"))
    location = relationship("Location")
    
    people = relationship("Person", secondary="person_fir_map", back_populates="firs_involved")

class PersonFIRMap(Base):
    __tablename__ = "person_fir_map"
    person_id = Column(Integer, ForeignKey("person.id"), primary_key=True)
    fir_id = Column(Integer, ForeignKey("fir.id"), primary_key=True)
    role = Column(String) # 'ACCUSED', 'VICTIM', 'WITNESS'

class Vehicle(Base):
    __tablename__ = "vehicle"
    id = Column(Integer, primary_key=True, autoincrement=True)
    registration_no = Column(String, unique=True, index=True)
    make_model = Column(String)
    owner_id = Column(Integer, ForeignKey("person.id"))
    owner = relationship("Person", back_populates="vehicles_owned")

class BankAccount(Base):
    __tablename__ = "bank_account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_no = Column(String, unique=True)
    bank_name = Column(String)
    person_id = Column(Integer, ForeignKey("person.id"))

class CaseManagement(Base):
    """
    The core workspace object. Aggregates the investigation.
    """
    __tablename__ = "case_management"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    status = Column(String, default="OPEN") # OPEN, CLOSED, PENDING
    assigned_officer = Column(String)
    primary_fir_id = Column(Integer, ForeignKey("fir.id"))
    
    ai_summary = Column(Text, nullable=True)
    investigation_notes = Column(Text, nullable=True)

def create_tables():
    # Ensure pgvector extension exists
    with engine.connect() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
