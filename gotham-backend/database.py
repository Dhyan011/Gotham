import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.schema import Table

# Database Setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://gotham:gotham_password@localhost:5432/gotham_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =====================================================================
# KSP OFFICIAL ER DIAGRAM SCHEMA (23 Tables + Junctions)
# =====================================================================

class State(Base):
    __tablename__ = "State"
    StateID = Column(Integer, primary_key=True)
    StateName = Column(String)
    NationalityID = Column(Integer)
    Active = Column(Boolean, default=True)

class District(Base):
    __tablename__ = "District"
    DistrictID = Column(Integer, primary_key=True)
    DistrictName = Column(String)
    StateID = Column(Integer, ForeignKey("State.StateID"))
    Active = Column(Boolean, default=True)

class UnitType(Base):
    __tablename__ = "UnitType"
    UnitTypeID = Column(Integer, primary_key=True)
    UnitTypeName = Column(String)
    CityDistState = Column(String)

class Unit(Base):
    __tablename__ = "Unit"
    UnitID = Column(Integer, primary_key=True)
    UnitName = Column(String)
    TypeID = Column(Integer, ForeignKey("UnitType.UnitTypeID"))
    ParentUnit = Column(Integer, ForeignKey("Unit.UnitID"), nullable=True)
    NationalityID = Column(Integer)
    StateID = Column(Integer, ForeignKey("State.StateID"))
    DistrictID = Column(Integer, ForeignKey("District.DistrictID"))
    Active = Column(Boolean, default=True)

class Court(Base):
    __tablename__ = "Court"
    CourtID = Column(Integer, primary_key=True)
    CourtName = Column(String)
    DistrictID = Column(Integer, ForeignKey("District.DistrictID"))
    StateID = Column(Integer, ForeignKey("State.StateID"))
    Active = Column(Boolean, default=True)

class Rank(Base):
    __tablename__ = "Rank"
    RankID = Column(Integer, primary_key=True)
    RankName = Column(String)
    Hierarchy = Column(Integer)
    Active = Column(Boolean, default=True)

class Designation(Base):
    __tablename__ = "Designation"
    DesignationID = Column(Integer, primary_key=True)
    DesignationName = Column(String)
    Active = Column(Boolean, default=True)
    SortOrder = Column(Integer)

class Employee(Base):
    __tablename__ = "Employee"
    EmployeeID = Column(Integer, primary_key=True)
    DistrictID = Column(Integer, ForeignKey("District.DistrictID"))
    UnitID = Column(Integer, ForeignKey("Unit.UnitID"))
    RankID = Column(Integer, ForeignKey("Rank.RankID"))
    DesignationID = Column(Integer, ForeignKey("Designation.DesignationID"))
    KGID = Column(String)
    FirstName = Column(String)
    EmployeeDOB = Column(Date)
    GenderID = Column(Integer)
    BloodGroupID = Column(Integer)
    PhysicallyChallenged = Column(Boolean)
    AppointmentDate = Column(Date)

class CrimeHead(Base):
    __tablename__ = "CrimeHead"
    CrimeHeadID = Column(Integer, primary_key=True)
    CrimeGroupName = Column(String)
    Active = Column(Boolean, default=True)

class CrimeSubHead(Base):
    __tablename__ = "CrimeSubHead"
    CrimeSubHeadID = Column(Integer, primary_key=True)
    CrimeHeadID = Column(Integer, ForeignKey("CrimeHead.CrimeHeadID"))
    CrimeHeadName = Column(String)
    SeqID = Column(Integer)

class CaseCategory(Base):
    __tablename__ = "CaseCategory"
    CaseCategoryID = Column(Integer, primary_key=True)
    CategoryName = Column(String)

class GravityOffence(Base):
    __tablename__ = "GravityOffence"
    GravityOffenceID = Column(Integer, primary_key=True)
    LookupValue = Column(String)

class CaseStatusMaster(Base):
    __tablename__ = "CaseStatusMaster"
    CaseStatusID = Column(Integer, primary_key=True)
    CaseStatusName = Column(String)

class CasteMaster(Base):
    __tablename__ = "CasteMaster"
    caste_master_id = Column(Integer, primary_key=True)
    caste_master_name = Column(String)

class ReligionMaster(Base):
    __tablename__ = "ReligionMaster"
    ReligionID = Column(Integer, primary_key=True)
    ReligionName = Column(String)

class OccupationMaster(Base):
    __tablename__ = "OccupationMaster"
    OccupationID = Column(Integer, primary_key=True)
    OccupationName = Column(String)

class Act(Base):
    __tablename__ = "Act"
    ActCode = Column(String, primary_key=True)
    ActDescription = Column(String)
    ShortName = Column(String)
    Active = Column(Boolean, default=True)

class Section(Base):
    __tablename__ = "Section"
    # Composite PK handling by making a unique surrogate or just mapping properly
    SectionID = Column(Integer, primary_key=True, autoincrement=True)
    ActCode = Column(String, ForeignKey("Act.ActCode"))
    SectionCode = Column(String)
    SectionDescription = Column(String)
    Active = Column(Boolean, default=True)

# ── Core CaseMaster Table ──
class CaseMaster(Base):
    __tablename__ = "CaseMaster"
    CaseMasterID = Column(Integer, primary_key=True)
    CrimeNo = Column(String)
    CaseNo = Column(String)
    CrimeRegisteredDate = Column(Date)
    PolicePersonID = Column(Integer, ForeignKey("Employee.EmployeeID"))
    PoliceStationID = Column(Integer, ForeignKey("Unit.UnitID"))
    CaseCategoryID = Column(Integer, ForeignKey("CaseCategory.CaseCategoryID"))
    GravityOffenceID = Column(Integer, ForeignKey("GravityOffence.GravityOffenceID"))
    CrimeMajorHeadID = Column(Integer, ForeignKey("CrimeHead.CrimeHeadID"))
    CrimeMinorHeadID = Column(Integer, ForeignKey("CrimeSubHead.CrimeSubHeadID"))
    CaseStatusID = Column(Integer, ForeignKey("CaseStatusMaster.CaseStatusID"))
    CourtID = Column(Integer, ForeignKey("Court.CourtID"), nullable=True)
    
    IncidentFromDate = Column(DateTime)
    IncidentToDate = Column(DateTime)
    InfoReceivedPSDate = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    BriefFacts = Column(Text)

class ActSectionAssociation(Base):
    __tablename__ = "ActSectionAssociation"
    AssocID = Column(Integer, primary_key=True, autoincrement=True)
    CaseMasterID = Column(Integer, ForeignKey("CaseMaster.CaseMasterID"))
    ActID = Column(String, ForeignKey("Act.ActCode"))
    SectionID = Column(Integer, ForeignKey("Section.SectionID"))
    ActOrderID = Column(Integer)
    SectionOrderID = Column(Integer)

class ComplainantDetails(Base):
    __tablename__ = "ComplainantDetails"
    ComplainantID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("CaseMaster.CaseMasterID"))
    ComplainantName = Column(String)
    AgeYear = Column(Integer)
    OccupationID = Column(Integer, ForeignKey("OccupationMaster.OccupationID"))
    ReligionID = Column(Integer, ForeignKey("ReligionMaster.ReligionID"))
    CasteID = Column(Integer, ForeignKey("CasteMaster.caste_master_id"))
    GenderID = Column(Integer)

class Victim(Base):
    __tablename__ = "Victim"
    VictimMasterID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("CaseMaster.CaseMasterID"))
    VictimName = Column(String)
    AgeYear = Column(Integer)
    GenderID = Column(Integer)
    VictimPolice = Column(String)

class Accused(Base):
    __tablename__ = "Accused"
    AccusedMasterID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("CaseMaster.CaseMasterID"))
    AccusedName = Column(String)
    AgeYear = Column(Integer)
    GenderID = Column(Integer)
    PersonID = Column(String) # E.g., A1, A2 for sorting

class ArrestSurrender(Base):
    __tablename__ = "ArrestSurrender"
    ArrestSurrenderID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("CaseMaster.CaseMasterID"))
    ArrestSurrenderTypeID = Column(Integer)
    ArrestSurrenderDate = Column(Date)
    ArrestSurrenderStateId = Column(Integer, ForeignKey("State.StateID"))
    ArrestSurrenderDistrictId = Column(Integer, ForeignKey("District.DistrictID"))
    PoliceStationID = Column(Integer, ForeignKey("Unit.UnitID"))
    IOID = Column(Integer, ForeignKey("Employee.EmployeeID"))
    CourtID = Column(Integer, ForeignKey("Court.CourtID"))
    AccusedMasterID = Column(Integer, ForeignKey("Accused.AccusedMasterID"))
    IsAccused = Column(Boolean)
    IsComplainantAccused = Column(Boolean)

# Junction for multiple accused per arrest event
inv_arrestsurrenderaccused = Table('inv_arrestsurrenderaccused', Base.metadata,
    Column('ArrestSurrenderID', Integer, ForeignKey('ArrestSurrender.ArrestSurrenderID')),
    Column('AccusedMasterID', Integer, ForeignKey('Accused.AccusedMasterID'))
)


# =====================================================================
# GOTHAM ANALYTICS LAYER (Custom extensions for AI/Graph)
# =====================================================================

class GOTHAM_ResolvedPerson(Base):
    """
    Generated by RapidFuzz Entity Resolution. Unifies multiple AccusedMasterID 
    rows into a single entity to feed into the Neo4j graph.
    """
    __tablename__ = "GOTHAM_ResolvedPerson"
    person_id = Column(Integer, primary_key=True, autoincrement=True)
    resolved_name = Column(String)
    risk_score = Column(Float, default=0.0)
    mo_pattern_tags = Column(String) # Comma separated
    primary_district = Column(Integer, ForeignKey("District.DistrictID"))

class GOTHAM_Person_Accused_Map(Base):
    """Junction mapping the resolved person to their raw FIR accused entries."""
    __tablename__ = "GOTHAM_Person_Accused_Map"
    map_id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey("GOTHAM_ResolvedPerson.person_id"))
    AccusedMasterID = Column(Integer, ForeignKey("Accused.AccusedMasterID"))


def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
