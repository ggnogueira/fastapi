import re
import jwt as _jwt
import datetime as _dt
import database as _database, models as _models, schemas as _schemas
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import fastapi as _fastapi
import fastapi.security as _security

oath2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")
JWT_SECRET = "myjwtsecret"


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()

async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    user_obj = _models.User(
        email=user.email,
        hashed_password=_hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(email, db)

    if not user:
        return False
    
    if not user.verify_password(password):
        return False
    
    return user

async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)

    token = _jwt.encode(
        user_obj.dict(),
        JWT_SECRET
    )
    return dict(access_token=token, token_type="bearer")

async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oath2schema)
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )
        
    return _schemas.User.from_orm(user)

async def create_lead(user: _schemas.User, db: _orm.Session, lead: _schemas.LeadCreate):
    lead = _models.Lead(**lead.dict(), owner_id = user.id)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return _schemas.Lead.from_orm(lead)

async def get_leads(user: _schemas.User, db: _orm.Session):
    leads = db.query(_models.Lead).filter_by(owner_id = user.id)
    return list(map(_schemas.Lead.from_orm, leads))

async def _lead_selector(lead_id: int, user: _schemas.User, db: _orm.Session):
    lead = (
        db.query(_models.Lead)
        .filter_by(owner_id=user.id)
        .filter(_models.Lead.id == lead_id).first()
    )

    if lead is None:
        raise _fastapi.HTTPException(status_code=404, detail="Lead not found")
    
    return lead

async def get_lead(lead_id: int, user: _schemas.User, db: _orm.Session):
    lead = await _lead_selector(lead_id=lead_id, user=user, db=db)

    return _schemas.Lead.from_orm(lead)

async def delete_lead(lead_id: int, user: _schemas.User, db: _orm.Session):
    lead = await _lead_selector(lead_id=lead_id, user=user, db=db)
    db.delete(lead)
    db.commit()

async def update_lead(lead_id: int, lead: _schemas.LeadCreate, user: _schemas.User, db: _orm.Session):
    lead_db = await _lead_selector(lead_id=lead_id, user=user, db=db)

    lead_db.first_name = lead.first_name
    lead_db.last_name = lead.last_name
    lead_db.email = lead.email
    lead_db.company = lead.company
    lead_db.note = lead.note
    lead_db.date_last_updated = _dt.datetime.utcnow()

    db.commit()
    db.refresh(lead_db)

    return _schemas.Lead.from_orm(lead_db)

async def create_code_system(user: _schemas.User, db: _orm.Session, code_system: _schemas.CodeSystemCreate):
    code_system = _models.CodeSystem(**code_system.dict(), owner_id = user.id)
    db.add(code_system)
    db.commit()
    db.refresh(code_system)
    return _schemas.CodeSystem.from_orm(code_system)

async def get_code_systems(user: _schemas.User, db: _orm.Session):
    code_systems = db.query(_models.CodeSystem).filter_by(owner_id = user.id)
    return list(map(_schemas.CodeSystem.from_orm, code_systems))

async def _code_system_selector(code_system_id: int, user: _schemas.User, db: _orm.Session):
    code_system = (
        db.query(_models.CodeSystem)
        .filter_by(owner_id=user.id)
        .filter(_models.CodeSystem.id == code_system_id).first()
    )

    if code_system is None:
        raise _fastapi.HTTPException(status_code=404, detail="Code System not found")
    
    return code_system

async def get_code_system(code_system_id: int, user: _schemas.User, db: _orm.Session):
    code_system = await _code_system_selector(code_system_id=code_system_id, user=user, db=db)

    return _schemas.CodeSystem.from_orm(code_system)

async def delete_code_system(code_system_id: int, user: _schemas.User, db: _orm.Session):
    code_system = await _code_system_selector(code_system_id=code_system_id, user=user, db=db)
    db.delete(code_system)
    db.commit()

async def update_code_system(code_system_id: int, code_system: _schemas.CodeSystemCreate, user: _schemas.User, db: _orm.Session):
    code_system_db = await _code_system_selector(code_system_id=code_system_id, user=user, db=db)

    code_system_db.version = code_system.version
    code_system_db.system = code_system.system
    code_system_db.name = code_system.name
    code_system_db.date_last_updated = _dt.datetime.utcnow()

    db.commit()
    db.refresh(code_system_db)

    return _schemas.CodeSystem.from_orm(code_system_db)

async def create_concept(code_system_id: int, user: _schemas.User, db: _orm.Session, concept: _schemas.ConceptCreate):
    code_system = await _code_system_selector(code_system_id=code_system_id, user=user, db=db)
    
    concept = _models.Concept(**concept.dict(), code_system_id = code_system.id)
    db.add(concept)
    db.commit()
    db.refresh(concept)
    return _schemas.Concept.from_orm(concept)

async def get_concepts(code_system_id: int, user: _schemas.User, db: _orm.Session):
    code_system = await _code_system_selector(code_system_id=code_system_id, user=user, db=db)

    concepts = db.query(_models.Concept).filter_by(code_system_id = code_system.id)
    return list(map(_schemas.Concept.from_orm, concepts))

async def _concept_selector(code: str, code_system: _schemas.CodeSystem, db: _orm.Session):
    concept = (
        db.query(_models.Concept)
        .filter_by(code_system_id=code_system.id)
        .filter(_models.Concept.code == code).first()
    )

    if concept is None:
        raise _fastapi.HTTPException(status_code=404, detail="Concept not found")
    
    return concept

async def get_concept(code: str, code_system_id: int, user: _schemas.User, db: _orm.Session):
    code_system = await _code_system_selector(code_system_id=code_system_id, user=user, db=db)

    concept = await _concept_selector(code=code, code_system=code_system, db=db)
    return _schemas.Concept.from_orm(concept)

async def delete_concept(code: str, code_system_id: int, user: _schemas.User, db: _orm.Session):
    code_system = await _code_system_selector(code_system_id=code_system_id, user=user, db=db)
    if code_system is None:
        raise _fastapi.HTTPException(status_code=404, detail="Code System not found")
    
    concept = await _concept_selector(code=code, code_system=code_system, db=db)
    db.delete(concept)
    db.commit()

async def update_concept(code: str, concept: _schemas.ConceptCreate, code_system_id: int, user: _schemas.User, db: _orm.Session):
    code_system = await _code_system_selector(code_system_id=code_system_id, user=user, db=db)
    if code_system is None:
        raise _fastapi.HTTPException(status_code=404, detail="Code System not found")
    
    concept_db = await _concept_selector(code=code, code_system=code_system, db=db)

    concept_db.code = concept.code
    concept_db.display = concept.display
    concept_db.date_last_updated = _dt.datetime.utcnow()

    db.commit()
    db.refresh(concept_db)

    return _schemas.Concept.from_orm(concept_db)