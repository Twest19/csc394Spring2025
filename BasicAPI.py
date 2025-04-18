# Tim West
# HW2 - API
# 3 Example endpoints - Documents, Users, Annotations

from fastapi import FastAPI

app = FastAPI()

document_one = {
    "pmcId": "11970135",
    "title": "Hand-to-surface bacterial transfer and healthcare-associated "
    "infections prevention: a pilot study on skin microbiome in a molecular biology laboratory "
}

document_two = {
    "pmcId": "40193249",
    "title": "Management of Staphylococcus aureus Bacteremia: A Review "
}

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
async def get_documents():
    return documents

# single get
@app.get("/documents/{pmc_id}")
async def get_document(pmc_id: str):
    docs = documents["results"]
    for doc in docs:
        # If this document has the PMC ID we're looking for
        if doc["pmcId"] == pmc_id:
            # Return this document
            return doc
        
    return {"error": f"Doc {pmc_id} not found"}, 404

# add a doc
@app.post("/documents")
async def add_document(doc: dict):
    pmc_id = doc["pmcId"]
    # Check if doc already exist - update it instead of creating duplicate
    for i, existing_doc in enumerate(documents["results"]):
        if existing_doc["pmcId"] == pmc_id:
            documents["results"][i] = doc
            return {"message": f"Document {pmc_id} was successfully updated."}
    
    documents["results"].append(doc)
    return {"message": f"Document {pmc_id} was successfully Added."}

# delete a doc
@app.delete("/documents/{pmc_id}")
async def delete_document(pmc_id: str):
    # Find doc to remove
    for i, existing_doc in enumerate(documents["results"]):
        if existing_doc["pmcId"] == pmc_id:
            documents["results"].pop(i)
            return {"message": f"Document {pmc_id} was successfully deleted"}
        
    return {"error": f"Document {pmc_id} not found"}, 404

    

## Users -
user = {
    "id": "user_123",
    "username": "researcher123",
    "email": "jdoe@depaul.edu",
    "first_name": "John",
    "last_name": "Doe",
    "institution": "DePaul University",
}

user2 = {
    "id": "user_444",
    "username": "someuser444",
    "email": "janedoe@depaul.edu",
    "first_name": "Jane",
    "last_name": "Doe",
    "institution": "DePaul University",
}

users = {
    "users" : [user, user2]
}

# Get all user
@app.get("/users/")
async def get_users():
    return users

# single user get
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    all_users = users["users"]
    for user in all_users:
        if user["id"] == user_id:
            return user
        
    return {"error": f"User {user_id} not found"}, 404

# add new user
@app.post("/users/")
async def add_user(user: dict):
    user_id = user["id"]
    # Check if user already exist - update user instead of creating duplicate
    for i, existing_user in enumerate(users["users"]):
        if existing_user["id"] == user_id:
            users["users"][i] = user
            return {"message": f"User {user_id} was successfully updated."}
        
    users["users"].append(user)
    return {"message": f"User {user_id} was successfully added."}

# delete a user
@app.delete("/users/{user_id}")
async def delete_user(user_id: str):    
    # Find the user to remove
    for i, existing_user in enumerate(users["users"]):
        if existing_user["id"] == user_id:
            users["users"].pop(i)
            return {"message": f"User {user_id} was successfully deleted"}
    
    return {"error": f"User {user_id} not found"}, 404



## Annotations - 
annotation = {
    "id": "anno_456789",
    "pmc_id": "11970135",
    "user_id": "user_123",
    "page_number": 1,
    "ai_summary": "Example Summary of document"
}

annotations = {
    "annotations" : [
        annotation
    ]
}

# single annotation get
@app.get("/annotations/{anno_id}")
async def get_annotation(anno_id: str):
    all_annos = annotations["annotations"]
    for anno in all_annos:
        if anno["id"] == anno_id:
            return anno
        
    return {"error": f"Annotation {anno_id} not found"}, 404

# add new annotation
@app.post("/annotations/")
async def add_annotation(anno: dict):
    anno_id = anno["id"]
    # Check if user already exist - update user instead of creating duplicate
    for i, existing_anno in enumerate(annotations["annotations"]):
        if existing_anno["id"] == anno_id:
            annotations["users"][i] = anno
            return {"message": f"Annotation {anno_id} was successfully updated."}
        
    annotations["annotations"].append(anno)
    return {"message": f"Annotation {anno_id} was successfully added."}

# delete annotation
@app.delete("/annotations/{anno_id}")
async def delete_annotation(anno_id: str):    
    # Find the annotation to remove
    for i, existing_anno in enumerate(annotations["annotations"]):
        if existing_anno["id"] == anno_id:
            annotations["annotations"].pop(i)
            user_id = existing_anno["user_id"]
            return {"message": f"Annotation deleted {anno_id} successfully deleted for user {user_id}"}
    
    return {"error": f"Annotation {anno_id} not found"}, 404
