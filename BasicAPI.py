# Tim West
# HW2 - API
# HW3 - External API Call
# 3 Example endpoints - Documents, Users, Annotations

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import random

from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import Column, Integer, String, create_engine

app = FastAPI()

# ---------- SQLite Setup ----------
SQLALCHEMY_DATABASE_URL = "sqlite:///./pubmed.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ---------- SQLite Setup ----------
class DocumentDB(Base):
    __tablename__ = "documents"
    pmcId = Column(String, primary_key=True, index=True)
    title = Column(String)

class UserDB(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    institution = Column(String)

class AnnotationDB(Base):
    __tablename__ = "annotations"
    id = Column(String, primary_key=True, index=True)
    pmc_id = Column(String)
    user_id = Column(String)
    page_number = Column(Integer)
    ai_summary = Column(String)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

class Document(BaseModel):
    pmcId: str
    title: str

    class Config:
        orm_mode = True


document_one = Document(
    pmcId="11970135",
    title="Hand-to-surface bacterial transfer and healthcare-associated "
    "infections prevention: a pilot study on skin microbiome in a molecular biology laboratory "
)

document_two = Document(
    pmcId="40193249",
    title="Management of Staphylococcus aureus Bacteremia: A Review")

# Mock Data
documents = {
    "info": {
    "count": 2,
    "pages": 1,
    "next": "",
    "prev": None
  },
  "results": [ 
      document_one, 
      document_two
    ]
}

## Documents -
# all get
@app.get("/documents")
async def get_documents(pmcid: str = None):
    with SessionLocal() as db:
        if pmcid:
            doc = db.query(DocumentDB).filter(DocumentDB.pmcId == pmcid).first()
            if doc:
                return doc
            return {"error": f"Doc {pmcid} not found"}, 404
        docs = db.query(DocumentDB).all()
        return docs
    

# Specific topic ID get
# HW 3 - add external API Call
# ex: /documents/random?topic=stroke
@app.get("/documents/random")
async def search_documents(topic: str = ""):
    rand_num = random.randint(1, 100)
    pmc_id_query = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={topic}&retmax={rand_num}&retmode=json"
    response = requests.get(pmc_id_query)
    data = response.json()
    pmc_ids = data["esearchresult"]["idlist"]

    rand_pmc_id = random.randint(0, len(pmc_ids) - 1)
    pmc_id = pmc_ids[rand_pmc_id]

    article_for_id = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&id={pmc_id}&retmode=json"
    response = requests.get(article_for_id)
    article_data = response.json()
    article = article_data["result"][pmc_id]
    title = article["title"]

    article_and_id = {
        "pmcId": pmc_id,
        "title": title
    }
    return article_and_id

# add a doc
@app.post("/documents")
async def add_document(doc: Document):
    with SessionLocal() as db:
        # Check if the document already exists in the database
        existing_doc = db.query(DocumentDB).filter(DocumentDB.pmcId == doc.pmcId).first()
        if existing_doc:
            # Update the existing document
            existing_doc = doc
            db.commit()
            return {"message": f"Document {doc.pmcId} was successfully updated."}
        
        # Add the new document to the database
        new_doc = DocumentDB(**doc.model_dump())
        db.add(new_doc)
        db.commit()
        return {"message": f"Document {doc.pmcId} was successfully added."}

# delete a doc
@app.delete("/documents")
async def delete_document(pmc_id: str):
    # Find doc to remove
    with SessionLocal() as db:
        existing_doc = db.query(DocumentDB).filter(DocumentDB.pmcId == pmc_id).first()
        if existing_doc:
            db.delete(existing_doc)
            db.commit()
            return {"message": f"Document {pmc_id} was successfully deleted"}
    # If doc not found, return error
    return {"error": f"Document {pmc_id} not found"}, 404



## Users -
class User(BaseModel):
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    institution: str

    class Config:
        orm_mode = True


user = User(
    id="user_123",
    username="researcher123",
    email="jdoe@depaul.edu",
    first_name="John",
    last_name="Doe",
    institution="DePaul University")

user2 = User(
    id="user_444",
    username="researcher444",
    email= "janedoe@depaul.edu",
    first_name="Jane",
    last_name="Doe",
    institution="DePaul University"
)

users = {
    "users" : [user, user2]
}

# Get all user
@app.get("/users")
async def get_users(response_model=User):
    with SessionLocal() as db:
        all_users = db.query(UserDB).all()
        return all_users


# single user get
@app.get("/user")
async def get_user(user_id: str, response_model=User):
    with SessionLocal() as db:
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if user:
            return user
    return {"error": f"User {user_id} not found"}, 404

# add new user
@app.post("/users")
async def add_user(user: User):
    user_id = user.id
    with SessionLocal() as db:
        # Check if the user already exists in the database
        existing_user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if existing_user:
            # Update the existing user
            existing_user = user
            db.commit()
            return {"message": f"User {user_id} was successfully updated."}
        
        # Add the new user to the database
        new_user = UserDB(**user.model_dump())
        db.add(new_user)
        db.commit()
        return {"message": f"User {user_id} was successfully added."}

# delete a user
@app.delete("/users")
async def delete_user(user_id: str):    

    with SessionLocal() as db:
        # Find the user to remove
        existing_user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if existing_user:
            db.delete(existing_user)
            db.commit()
            return {"message": f"User {user_id} was successfully deleted"}
    return {"error": f"User {user_id} not found"}, 404

## Annotations - 

class Annotation(BaseModel):
    id: str
    pmc_id: str
    user_id: str
    page_number: int
    ai_summary: str

    class Config:
        orm_mode = True


annotation = Annotation(
    id="anno_456789",
    pmc_id="11970135",
    user_id="user_123",
    page_number=1,
    ai_summary="Example Summary of document")

annotations = {
    "annotations" : [
        annotation
    ]
}

# single annotation get
@app.get("/annotations")
async def get_annotation(anno_id: str, response_model=Annotation):
    with SessionLocal() as db:
        # Find the annotation in the database
        existing_anno = db.query(AnnotationDB).filter(AnnotationDB.id == anno_id).first()
        if existing_anno:
            return existing_anno
    return {"error": f"Annotation {anno_id} not found"}, 404

# add new annotation
@app.post("/annotations")
async def add_annotation(anno: Annotation):
    anno_id = anno.id
    with SessionLocal() as db:
        # Check if the annotation already exists in the database
        existing_anno = db.query(AnnotationDB).filter(AnnotationDB.id == anno_id).first()
        if existing_anno:
            # Update the existing annotation
            existing_anno = anno
            
            db.commit()
            return {"message": f"Annotation {anno_id} was successfully updated."}
        
        # Add the new annotation to the database
        new_anno = AnnotationDB(**anno.model_dump())
        db.add(new_anno)
        db.commit()
        return {"message": f"Annotation {anno_id} was successfully added."}

# delete annotation
@app.delete("/annotations")
async def delete_annotation(anno_id: str):    
    # Find the annotation to remove
    with SessionLocal() as db:
        existing_anno = db.query(AnnotationDB).filter(AnnotationDB.id == anno_id).first()
        if existing_anno:
            db.delete(existing_anno)
            db.commit()
            return {"message": f"Annotation {anno_id} was successfully deleted"}
    return {"error": f"Annotation {anno_id} not found"}, 404
