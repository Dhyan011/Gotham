import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from pgvector.sqlalchemy import Vector

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://gotham:gotham_password@localhost:5432/gotham_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =====================================================================
# OFFICIAL PDF DB SCHEMA
# =====================================================================

class CaseMaster(Base):
    __tablename__ = "case_master"
    CaseMasterID = Column(Integer, primary_key=True, autoincrement=True)
    CrimeNo = Column(String, unique=True, index=True)
    CaseNo = Column(String)
    CrimeRegisteredDate = Column(Date)
    PolicePersonID = Column(Integer) # Mock FK
    PoliceStationID = Column(Integer) # Mock FK
    CaseCategoryID = Column(Integer)
    GravityOffenceID = Column(Integer)
    CrimeMajorHeadID = Column(Integer)
    CrimeMinorHeadID = Column(Integer)
    CaseStatusID = Column(Integer)
    CourtID = Column(Integer)
    
    IncidentFromDate = Column(DateTime)
    IncidentToDate = Column(DateTime)
    InfoReceivedPSDate = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    BriefFacts = Column(Text)
    
    # NLP / ML Enhancements (Not in PDF, added for Gotham)
    embedding = Column(Vector(384)) # Semantic search vector on BriefFacts
    
    # Relationships
    victims = relationship("Victim", back_populates="case")
    accused = relationship("Accused", back_populates="case")
    complainants = relationship("ComplainantDetails", back_populates="case")
    arrests = relationship("ArrestSurrender", back_populates="case")

class ComplainantDetails(Base):
    __tablename__ = "complainant_details"
    ComplainantID = Column(Integer, primary_key=True, autoincrement=True)
    CaseMasterID = Column(Integer, ForeignKey("case_master.CaseMasterID"))
    ComplainantName = Column(String)
    AgeYear = Column(Integer)
    OccupationID = Column(Integer)
    ReligionID = Column(Integer)
    CasteID = Column(Integer)
    GenderID = Column(Integer)
    
    case = relationship("CaseMaster", back_populates="complainants")

class Victim(Base):
    __tablename__ = "victim"
    VictimMasterID = Column(Integer, primary_key=True, autoincrement=True)
    CaseMasterID = Column(Integer, ForeignKey("case_master.CaseMasterID"))
    VictimName = Column(String)
    AgeYear = Column(Integer)
    GenderID = Column(Integer)
    VictimPolice = Column(String)
    
    case = relationship("CaseMaster", back_populates="victims")

class Accused(Base):
    __tablename__ = "accused"
    AccusedMasterID = Column(Integer, primary_key=True, autoincrement=True)
    CaseMasterID = Column(Integer, ForeignKey("case_master.CaseMasterID"))
    AccusedName = Column(String, index=True)
    AgeYear = Column(Integer)
    GenderID = Column(Integer)
    PersonID = Column(String) # Sorting ID A1, A2
    
    case = relationship("CaseMaster", back_populates="accused")
    arrests = relationship("ArrestSurrender", back_populates="accused")

class ArrestSurrender(Base):
    __tablename__ = "arrest_surrender"
    ArrestSurrenderID = Column(Integer, primary_key=True, autoincrement=True)
    CaseMasterID = Column(Integer, ForeignKey("case_master.CaseMasterID"))
    ArrestSurrenderTypeID = Column(Integer)
    ArrestSurrenderDate = Column(Date)
    ArrestSurrenderStateId = Column(Integer)
    ArrestSurrenderDistrictId = Column(Integer)
    PoliceStationID = Column(Integer)
    IOID = Column(Integer)
    CourtID = Column(Integer)
    AccusedMasterID = Column(Integer, ForeignKey("accused.AccusedMasterID"))
    IsAccused = Column(Boolean)
    IsComplainantAccused = Column(Boolean)
    
    case = relationship("CaseMaster", back_populates="arrests")
    accused = relationship("Accused", back_populates="arrests")

def create_tables():
    with engine.connect() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    Base.metadata.drop_all(bind=engine) # Drop old simple schema for the new robust one
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
