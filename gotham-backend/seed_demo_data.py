"""
GOTHAM Hackathon Seed Data Generator
Builds a hyper-connected, demo-perfect 30-node graph for Postgres & Neo4j.
Specifically builds the "Golden Demo" path around FIR-1245 and a White SUV gang.
"""
import os
import random
from datetime import datetime, timedelta
from database import SessionLocal, Person, FIR, Vehicle, Location, BankAccount, PersonFIRMap, CaseManagement, create_tables
from neo4j import GraphDatabase
import numpy as np

# Hardcoded vectors for demo semantic search (mock embeddings)
def mock_embedding():
    return np.random.rand(384).tolist()

def seed_postgres():
    db = SessionLocal()
    
    # 1. Locations
    mg_road = Location(address="MG Road, Bengaluru", latitude=12.9716, longitude=77.6013)
    indiranagar = Location(address="Indiranagar, Bengaluru", latitude=12.9784, longitude=77.6408)
    db.add_all([mg_road, indiranagar])
    db.commit()

    # 2. People (The "White SUV Gang")
    p1 = Person(name="Ravi Kumar", age=34, gender="M", risk_score=85.0) # Gang Leader
    p2 = Person(name="Suresh M", age=28, gender="M", risk_score=72.0)
    p3 = Person(name="Kiran Patel", age=41, gender="M", risk_score=91.0)
    
    # Innocent Bystander
    p4 = Person(name="Amit Sharma", age=45, gender="M", risk_score=12.0)
    db.add_all([p1, p2, p3, p4])
    db.commit()

    # 3. Vehicles
    v1 = Vehicle(registration_no="KA-01-AB-1234", make_model="White SUV - Mahindra Scorpio", owner_id=p1.id)
    v2 = Vehicle(registration_no="KA-05-XY-9999", make_model="Black Sedan - Honda City", owner_id=p4.id)
    db.add_all([v1, v2])
    db.commit()

    # 4. FIRs (The Golden Demo Target: FIR-1245)
    f1 = FIR(
        crime_no="FIR-1245", 
        date_registered=datetime.now() - timedelta(days=2),
        crime_type="Armed Robbery",
        description="Masked men escaped in a White SUV after robbing a jewelry store near MG Road.",
        location_id=mg_road.id,
        embedding=mock_embedding()
    )
    f2 = FIR(
        crime_no="FIR-1246",
        date_registered=datetime.now() - timedelta(days=15),
        crime_type="Extortion",
        description="Business owner threatened by two men near Indiranagar. Suspects fled in a white SUV.",
        location_id=indiranagar.id,
        embedding=mock_embedding()
    )
    db.add_all([f1, f2])
    db.commit()

    # 5. Mappings (Graph Edges)
    db.add(PersonFIRMap(person_id=p2.id, fir_id=f1.id, role="ACCUSED"))
    db.add(PersonFIRMap(person_id=p3.id, fir_id=f1.id, role="ACCUSED"))
    db.add(PersonFIRMap(person_id=p1.id, fir_id=f2.id, role="ACCUSED")) # Leader connected to older crime
    db.add(PersonFIRMap(person_id=p4.id, fir_id=f1.id, role="VICTIM")) # Innocent bystander
    db.commit()

    # 6. Case Management Workspace
    c1 = CaseManagement(
        title="Operation MG Road Syndicate",
        status="OPEN",
        assigned_officer="Inspector Raj",
        primary_fir_id=f1.id,
        investigation_notes="Looking for connections between the recent MG Road robbery and older Indiranagar extortions."
    )
    db.add(c1)
    db.commit()
    db.close()
    print("Postgres seeded successfully!")

def seed_neo4j():
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "gotham_graph_pass"
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    cypher_queries = [
        "MATCH (n) DETACH DELETE n;", # Clear DB
        # Create Nodes
        "CREATE (p1:Person {name: 'Ravi Kumar', risk_score: 85.0})",
        "CREATE (p2:Person {name: 'Suresh M', risk_score: 72.0})",
        "CREATE (p3:Person {name: 'Kiran Patel', risk_score: 91.0})",
        "CREATE (p4:Person {name: 'Amit Sharma', risk_score: 12.0})",
        
        "CREATE (v1:Vehicle {reg: 'KA-01-AB-1234', model: 'White SUV'})",
        "CREATE (v2:Vehicle {reg: 'KA-05-XY-9999', model: 'Black Sedan'})",
        
        "CREATE (f1:FIR {crime_no: 'FIR-1245', type: 'Armed Robbery'})",
        "CREATE (f2:FIR {crime_no: 'FIR-1246', type: 'Extortion'})",
        
        "CREATE (l1:Location {name: 'MG Road'})",
        "CREATE (l2:Location {name: 'Indiranagar'})",

        # Create Edges (Ontology)
        "MATCH (p:Person {name: 'Ravi Kumar'}), (v:Vehicle {reg: 'KA-01-AB-1234'}) CREATE (p)-[:OWNS]->(v)",
        "MATCH (p:Person {name: 'Amit Sharma'}), (v:Vehicle {reg: 'KA-05-XY-9999'}) CREATE (p)-[:OWNS]->(v)",
        
        "MATCH (p:Person {name: 'Suresh M'}), (f:FIR {crime_no: 'FIR-1245'}) CREATE (p)-[:ACCUSED_IN]->(f)",
        "MATCH (p:Person {name: 'Kiran Patel'}), (f:FIR {crime_no: 'FIR-1245'}) CREATE (p)-[:ACCUSED_IN]->(f)",
        "MATCH (p:Person {name: 'Ravi Kumar'}), (f:FIR {crime_no: 'FIR-1246'}) CREATE (p)-[:ACCUSED_IN]->(f)",
        
        "MATCH (v:Vehicle {reg: 'KA-01-AB-1234'}), (f:FIR {crime_no: 'FIR-1245'}) CREATE (v)-[:USED_IN]->(f)",
        "MATCH (v:Vehicle {reg: 'KA-01-AB-1234'}), (f:FIR {crime_no: 'FIR-1246'}) CREATE (v)-[:USED_IN]->(f)",
        
        "MATCH (f:FIR {crime_no: 'FIR-1245'}), (l:Location {name: 'MG Road'}) CREATE (f)-[:OCCURRED_AT]->(l)",
        "MATCH (f:FIR {crime_no: 'FIR-1246'}), (l:Location {name: 'Indiranagar'}) CREATE (f)-[:OCCURRED_AT]->(l)",
    ]

    with driver.session() as session:
        for q in cypher_queries:
            session.run(q)
            
    print("Neo4j seeded successfully!")
    driver.close()

if __name__ == "__main__":
    print("Creating tables...")
    create_tables()
    print("Seeding Postgres...")
    seed_postgres()
    print("Seeding Neo4j...")
    seed_neo4j()
    print("Demo Data Seed Complete!")
