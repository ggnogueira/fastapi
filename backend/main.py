from typing import List
import fastapi as _fastapi
import fastapi.security as _security

import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas

app = _fastapi.FastAPI()

@app.post("/api/users")
async def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="User with this email already exists in the database")
    
    user = await _services.create_user(user, db)

    return await _services.create_token(user)

@app.post("/api/token")
async def generate_token(form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Incorrect email or password")
    return await _services.create_token(user)

@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user

@app.post("/api/leads", response_model=_schemas.Lead)
async def create_lead(lead: _schemas.LeadCreate, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.create_lead(user=user, db=db, lead=lead)

@app.get("/api/leads", response_model=List[_schemas.Lead])
async def get_leads(user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_leads(user=user, db=db)

@app.get("/api/leads/{lead_id}", status_code=200)
async def get_lead(lead_id: int, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_lead(lead_id=lead_id, user=user, db=db)

@app.delete("/api/leads/{lead_id}", status_code=204)
async def delete_lead(lead_id: int, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    await _services.delete_lead(lead_id=lead_id, user=user, db=db)
    return {"message": "Successfully Deleted"}

@app.put("/api/leads/{lead_id}", status_code=200)
async def update_lead(lead_id: int, lead: _schemas.LeadCreate, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    await _services.update_lead(lead_id=lead_id, lead=lead, user=user, db=db)
    return {"message": "Successfully Updated"}

@app.post("/api/codesystems", response_model=_schemas.CodeSystem)
async def create_code_system(code_system: _schemas.CodeSystemCreate, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.create_code_system(user=user, db=db, code_system=code_system)

@app.get("/api/codesystems", response_model=List[_schemas.CodeSystem])
async def get_code_systems(user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_code_systems(user=user, db=db)

@app.get("/api/codesystems/{code_system_id}", status_code=200)
async def get_code_system(code_system_id: int, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_code_system(code_system_id=code_system_id, user=user, db=db)

@app.delete("/api/codesystems/{code_system_id}", status_code=204)
async def delete_code_system(code_system_id: int, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    await _services.delete_code_system(code_system_id=code_system_id, user=user, db=db)
    return {"message": "Successfully Deleted"}

@app.put("/api/codesystems/{code_system_id}", status_code=200)
async def update_code_system(code_system_id: int, code_system: _schemas.CodeSystemCreate, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    await _services.update_code_system(code_system_id=code_system_id, code_system=code_system, user=user, db=db)
    return {"message": "Successfully Updated"}

@app.post("/api/concepts", response_model=_schemas.Concept)
async def create_concept(concept: _schemas.ConceptCreate, code_system_id: int, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.create_concept(code_system_id=code_system_id, db=db, concept=concept, user=user)

@app.get("/api/concepts", response_model=List[_schemas.Concept])
async def get_concepts(code_system_id: int, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_concepts(code_system_id=code_system_id, user=user, db=db)

@app.get("/api/concepts/{code_system_id}/{code}", status_code=200)
async def get_concept(code: str, code_system_id: int, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_concept(code=code, code_system_id=code_system_id, user=user, db=db)

@app.delete("/api/concepts/{code_system_id}/{code}", status_code=204)
async def delete_concept(code: str, code_system_id: int, user: _schemas.User  = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    await _services.delete_concept(code=code, code_system_id=code_system_id, user=user, db=db)
    return {"message": "Successfully Updated"}

@app.put("/api/concepts/{code_system_id}/{code}", status_code=200)
async def update_concept(code: str, concept: _schemas.ConceptCreate, code_system_id: int, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    await _services.update_concept(code=code, code_system_id=code_system_id, concept=concept, user=user, db=db)
    return {"message": "Successfully Updated"}


@app.get("/api")
async def root():
    return {"message": "Code System Manager"}
