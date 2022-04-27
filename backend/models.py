import datetime as _dt
from turtle import back
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import database as _database

class User(_database.Base):
    __tablename__ = "users"
    #id = _sql.Column(_sql.Integer, primary_key=True, autoincrement=True)
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)

    leads = _orm.relationship("Lead", back_populates="owner")
    code_systems = _orm.relationship("CodeSystem", back_populates="owner")
    
    def verify_password(self, password):
        return _hash.bcrypt.verify(password, self.hashed_password)

class Lead(_database.Base):
    __tablename__ = "leads"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    first_name = _sql.Column(_sql.String, index=True)
    last_name = _sql.Column(_sql.String, index=True)
    email = _sql.Column(_sql.String, index=True)
    company = _sql.Column(_sql.String, index=True, default="")
    note = _sql.Column(_sql.String, default="")
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow, onupdate=_dt.datetime.utcnow)

    owner = _orm.relationship("User", back_populates="leads")

class CodeSystem(_database.Base):
    __tablename__ = "code_systems"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    version = _sql.Column(_sql.String, index=True)
    system = _sql.Column(_sql.String, index=True)
    name = _sql.Column(_sql.String, index=True)  
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow, onupdate=_dt.datetime.utcnow)

    concepts = _orm.relationship("Concept", back_populates="code_system")
    owner = _orm.relationship("User", back_populates="code_systems")

class Concept(_database.Base):
    __tablename__ = "concepts"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    code = _sql.Column(_sql.String, index=True)
    code_system_id = _sql.Column(_sql.Integer, _sql.ForeignKey("code_systems.id"))
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow, onupdate=_dt.datetime.utcnow)

    code_system = _orm.relationship("CodeSystem", back_populates="concepts")