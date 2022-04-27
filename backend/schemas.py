import datetime as _dt
import pydantic as _pydantic

class _UserBase(_pydantic.BaseModel):
    email: str

class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True

class User(_UserBase):
    id: int

    class Config:
        orm_mode = True

class _LeadBase(_pydantic.BaseModel):
    first_name: str
    last_name: str
    email: str
    company: str
    note: str

class LeadCreate(_LeadBase):
    pass

class Lead(_LeadBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True

class _CodeSystemBase(_pydantic.BaseModel):
    version: str
    system: str
    name: str

class CodeSystemCreate(_CodeSystemBase):
    pass

class CodeSystem(_CodeSystemBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True

class _ConceptBase(_pydantic.BaseModel):
    code: str
    display: str

class ConceptCreate(_ConceptBase):
    pass

class Concept(_ConceptBase):
    id: int
    code_system_id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True
